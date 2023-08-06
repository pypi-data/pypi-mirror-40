# -*- coding: utf-8 -*-
# S3FileStore
#
# Client code (remote file list control and S3 worker thread) use one of these
# to get information about the current remote directory, especially the list of
# files.  They use setRemoteDir to change directory.
#
# TODO switch to dictionaries
import os
import time
import threading
import tempfile
import Utils
from Utils import DEBUG
from FileCrypto import DecryptStr
from FileCrypto import EncryptStr
from FileCrypto import DecryptFile
from FileCrypto import EncryptFile
from boto.s3.connection import S3Connection
from boto.exception import S3ResponseError
from boto.s3.key import Key
from base64 import b64decode
from base64 import b64encode
from passlib.hash import pbkdf2_sha256
from ast import literal_eval
from itertools import chain


class S3FileStore:
    FOLDER_CONTENTS_HEADER = 'Nuvovis Cloud Filer folder contents:' # const

    def __init__(self, actionHandler):
        DEBUG('S3FileStore.__init__')
        self.__actionHandler = actionHandler
        self.__connected = False
        self.__cancelling = False
        self.__transferStateLock = threading.Lock()


    def connect(self, accessKey, secretKey, password, cloudHost, cloudRootText):
        DEBUG('S3FileStore.connect: cloudHost=' + cloudHost)
        DEBUG('S3FileStore.connect: cloudRootText=' + cloudRootText)
        return self.setConnection(S3Connection(accessKey, secretKey, host=cloudHost, is_secure=False), cloudRootText, password)


    def setConnection(self, connection, cloudRootText, password):
        DEBUG('S3FileStore.setConnection: cloudRootText=' + cloudRootText)
        self.__connection = connection
        self.__cloudRootText = cloudRootText
        self.__buckets = self.__connection.get_all_buckets()
        self.__currentRemotePath = self.__cloudRootText + '/'
        self.__currentRemoteCryptoPath = self.__cloudRootText + '/'
        self.__currentBucket = None
        self.__currentDirKeys = '/'
        self.__password = password
        self.__dirContentsNeedsRefresh = True
        self.__encryptionKey = ''
        self.__salt = ''
        self.__connected = True
        self.__transferInProgress = False
        return self.__connection


    def isCurrentFolderRoot(self):
        return self.__currentRemotePath.rstrip('/') == self.__cloudRootText


    def isCurrentFolderEncrypted(self):
        if self.isCurrentFolderRoot():
            return False # At root bucket list always cleartext
        else:
            return self.__password


    def getEncryptionKey(self):
        return self.__encryptionKey


    def addCryptoFile(self, cryptoFileName, newFileName, fileSize, lastModTime):
        DEBUG('S3FileStore.addCryptoFile: cryptoFileName=' + cryptoFileName)
        DEBUG('S3FileStore.addCryptoFile: newFileName=' + newFileName)
        self.__cryptoFiles.append((cryptoFileName, newFileName, fileSize, lastModTime))


    def addCryptoDir(self, cryptoFolderName, newFolderName):
        DEBUG('S3FileStore.addCryptoDir: cryptoFolderName=' + cryptoFolderName)
        DEBUG('S3FileStore.addCryptoDir: newFolderName=' + newFolderName)
        self.__cryptoDirs.append((cryptoFolderName, newFolderName, '0', '0'))


    def getNewCryptoFileName(self):
        if len(self.__cryptoFileHoles) > 0:
            newNum = self.__cryptoFileHoles[0]
            self.__cryptoFileHoles = self.__cryptoFileHoles[1:]
        else:
            newNum = self.__cryptoFileNextFree
            self.__cryptoFileNextFree = self.__cryptoFileNextFree + 1

        newName = "_CFL%07d" % (newNum)
        DEBUG('S3FileStore.getNewCryptoFileName: newName=' + newName)
        return newName

           
    def getNewCryptoFolderName(self):
        if len(self.__cryptoDirHoles) > 0:
            newNum = self.__cryptoDirHoles[0]
            self.__cryptoDirHoles = self.__cryptoDirHoles[1:]
        else:
            newNum = self.__cryptoDirNextFree
            self.__cryptoDirNextFree = self.__cryptoDirNextFree + 1

        newName = "_CFD%07d" % (newNum)
        DEBUG('S3FileStore.getNewCryptoFolderName: newName=' + newName)
        return newName

           
    def getAndRemoveExistingCryptoFileName(self, cleartextFileName):
        DEBUG('S3FileStore.getAndRemoveExistingCryptoFileName: cleartextFileName=' + cleartextFileName)
        fileNameList = filter(lambda (s1, s2, s3, s4): s2 == cleartextFileName, self.__cryptoFiles)
        self.__cryptoFiles = filter(lambda (s1, s2, s3, s4): s2 != cleartextFileName, self.__cryptoFiles)
        DEBUG('S3FileStore.getAndRemoveExistingCryptoFileName: __cryptoFiles=' + str(self.__cryptoFiles))
        if len(fileNameList) == 0:
            DEBUG('S3FileStore.getAndRemoveExistingCryptoFileName: not found')
            return None
        else:
            (s1, s2, s3, s4) = fileNameList[0]
            DEBUG('S3FileStore.getAndRemoveExistingCryptoFileName: found ' + s1)
            return s1


    def getAndRemoveExistingCryptoDirName(self, cleartextDirName):
        DEBUG('getAndRemoveExistingCryptoDirName: cleartextDirName=' + cleartextDirName)
        dirNameList = filter(lambda (s1, s2, s3, s4): s2 == cleartextDirName, self.__cryptoDirs)
        self.__cryptoDirs = filter(lambda (s1, s2, s3, s4): s2 != cleartextDirName, self.__cryptoDirs)
        DEBUG('getAndRemoveExistingCryptoDirName: cryptoDirs=' + str(self.__cryptoDirs))
        if len(dirNameList) == 0:
            DEBUG('getAndRemoveExistingCryptoDirName: not found')
            return None
        else:
            (s1, s2, s3, s4) = dirNameList[0]
            DEBUG('getAndRemoveExistingCryptoDirName: found ' + s1)
            return s1


    def __setRelativeRemoteDir(self, newDir):
        DEBUG('S3FileStore.__setRelativeRemoteDir: newDir=' + newDir)
        if not self.__connected:
            raise Exception('S3FileStore.__setRelativeRemoteDir: not connected')
        if newDir.startswith(self.__cloudRootText):
            raise Exception('S3FileStore.__setRelativeRemoteDir: absolute path found - newDir=' + newDir)
        if not self.__currentRemotePath:
            raise Exception('S3FileStore.__setRelativeRemoteDir: invalid current remote path')

        self.__currentRemotePath = self.__currentRemotePath.rstrip('/')
        self.__currentRemoteCryptoPath = self.__currentRemoteCryptoPath.rstrip('/')
        newDir = newDir.rstrip('/')
        # If the new dir is depth of 1 cd newDir else step into each level of sub-folder
        if '/' not in newDir:
            if newDir == '..':
                currentPathBits = self.__currentRemotePath.split('/')
                self.__currentRemotePath = '/'.join(currentPathBits[:len(currentPathBits)-1])
                if self.__currentRemotePath == self.__cloudRootText:
                    self.__currentRemotePath += '/'
                    self.__currentRemoteCryptoPath = self.__currentRemotePath
                if self.isCurrentFolderEncrypted():
                    currentCryptoPathBits = self.__currentRemoteCryptoPath.split('/')
                    self.__currentRemoteCryptoPath = '/'.join(currentCryptoPathBits[:len(currentCryptoPathBits)-1])
                    self.__loadEncryptedDirContents()
                else:
                    self.__loadCleartextDirContents()
            else:
                self.__currentRemotePath = self.__currentRemotePath + '/' + newDir
                if self.isCurrentFolderEncrypted():
                    bucket, keyName = self.getCurrentRemoteLocation()
                    if bucket:
                        DEBUG('S3FileStore.__setRelativeRemoteDir: bucket = ' + bucket.name)
                        self.__currentRemoteCryptoPath = self.__currentRemoteCryptoPath + '/' + self.getCryptoFolderName(newDir)
                    else:
                        DEBUG('S3FileStore.__setRelativeRemoteDir: at root')
                        self.__currentRemoteCryptoPath = self.__currentRemoteCryptoPath + '/' + newDir
                    self.__loadEncryptedDirContents()
                else:
                    self.__loadCleartextDirContents()
            DEBUG('S3FileStore.__setRelativeRemoteDir: _currentRemotePath = ' + self.__currentRemotePath)
            DEBUG('S3FileStore.__setRelativeRemoteDir: _currentRemoteCryptoPath = ' + self.__currentRemoteCryptoPath)
        else:
            newPathBits = newDir.split('/', 1)
            assert (len(newPathBits)==2), "newPathBits len <> 2"
            self.__setRelativeRemoteDir(newPathBits[0]) # Head
            self.__setRelativeRemoteDir(newPathBits[1]) # Tail


    def setRemoteDir(self, newDir):
        DEBUG('S3FileStore.setRemoteDir: newDir=' + newDir)
        if not self.__connected:
            raise Exception('S3FileStore.setRemoteDir: not connected')
        DEBUG('S3FileStore.setRemoteDir: self.__currentRemotePath=' + self.__currentRemotePath)
        if self.__currentRemotePath == newDir:
            DEBUG('S3FileStore.setRemoteDir: already there!')
            return

        # If we are passed an absolute path
        if newDir.startswith(self.__cloudRootText + '/'):
            DEBUG('S3FileStore.setRemoteDir: we were passed an absolute path')
            newDir = newDir[len(self.__cloudRootText + '/'):]
            self.__currentBucket = None
            self.__currentRemotePath = self.__cloudRootText
            self.__currentRemoteCryptoPath = self.__cloudRootText

        self.__setRelativeRemoteDir(newDir)
        self.__actionHandler.doneAction('cd ' + newDir)


    def __getBucket(self, bucketName):
        DEBUG('S3FileStore.__getBucket: bucketName=' + bucketName)
        for bucket in self.__buckets:
            if bucket.name == bucketName:
                return bucket

        raise Exception('S3FileStore.__getBucket: bucket not found - bucketName=' + bucketName)


    def getCurrentRemotePath(self):
        return self.__currentRemotePath


    def getCurrentRemoteLocation(self):
        return self.__currentBucket, self.__currentDirKeys


    def __setCurrentRemoteLocation(self):
        """Split the current remote location string of the form
        CloudHeader/BucketName/FolderPath (e.g. GC:/MyBucket/Backups/24May2018)
        into the bucket object and the folder path string.
        """
        if self.isCurrentFolderEncrypted():
            DEBUG('S3FileStore.__setCurrentRemoteLocation: currentRemoteCryptoPath=' + self.__currentRemoteCryptoPath)
            pathBits = self.__currentRemoteCryptoPath.split('/')
        else:
            DEBUG('S3FileStore.__setCurrentRemoteLocation: currentRemotePath=' + self.__currentRemotePath)
            pathBits = self.__currentRemotePath.split('/')
        # If at root: list of buckets
        if len(pathBits) < 2 or pathBits[1] == '':
            DEBUG('S3FileStore.__setCurrentRemoteLocation: at root - pathBits=' + str(pathBits))
            if pathBits[1] == '':
                assert len(pathBits) == 2
            self.__currentBucket = None
            self.__currentDirKeys = '/'
        else:
            DEBUG('S3FileStore.__setCurrentRemoteLocation: pathBits=' + str(pathBits))
            bucketName = pathBits[1]
            if len(pathBits) > 2:
                keyName = '/'.join(pathBits[2:]) + '/'
            else:
                keyName = '/'
            self.__currentBucket = self.__getBucket(bucketName)
            self.__currentDirKeys = keyName


    def deleteFile(self, fileName):
        DEBUG('S3FileStore.deleteFile: fileName=' + fileName)
        DEBUG('S3FileStore.deleteFile: self.__currentBucket.name=' + self.__currentBucket.name)
        DEBUG('S3FileStore.deleteFile: self.__currentDirKeys=' + self.__currentDirKeys)
        if self.isCurrentFolderEncrypted():
            fileName = self.getAndRemoveExistingCryptoFileName(fileName)
            self.uploadNewContentsInfo(self.__currentBucket, self.__currentDirKeys)
        
        k = Key(self.__currentBucket)
        k.key = self.__currentDirKeys + fileName
        DEBUG('S3FileStore.deleteFile: k=' + str(k))
        k.delete()
        self.__dirContentsNeedsRefresh = True
        self.__actionHandler.doneAction('Deleted ' + fileName)


    def __recursiveList(self, bucket, keyName):
        keys = bucket.list(keyName, '/')
        for key in keys:
            DEBUG('key.name=' + key.name)
            if key.name.endswith('/'):
                keys2 = self.__recursiveList(bucket, key.name)
                keys = chain(keys, keys2)

        return keys


    def deleteFolder(self, dirName):
        DEBUG('S3FileStore.deleteFolder: dirName=' + dirName)
        self.__actionHandler.doneAction('Deleting ' + dirName + '...')
        if self.isCurrentFolderEncrypted():
            dirName = self.getAndRemoveExistingCryptoDirName(dirName)
            self.uploadNewContentsInfo(self.__currentBucket, self.__currentDirKeys)

        keyName = self.__currentDirKeys.lstrip('/') + dirName + '/'
        DEBUG('S3FileStore.deleteFolder: List folder for deletion: prefix = ' + keyName)
        keys = self.__recursiveList(self.__currentBucket, keyName)
        for key in keys:
            DEBUG('S3FileStore.deleteFile: key.name=' + key.name)
            if key.name.endswith('/'):
                DEBUG('S3FileStore.deleteFolder: Ignoring dir')
                continue
            key.delete()

        self.__dirContentsNeedsRefresh = True
        self.__actionHandler.doneAction('Deleted ' + dirName)


    def transferReset(self):
        DEBUG('S3FileStore.transferReset')
        self.__transferStateLock.acquire()
        self.__cancelling = False
        self.__transferInProgress = False
        self.__transferStateLock.release()


    def __startTransferOpen(self, filePath, mode):
        DEBUG('S3FileStore.__startTransferOpen: filePath=' + filePath)
        DEBUG('S3FileStore.__startTransferOpen: mode=' + str(mode))
        self.__transferStateLock.acquire()
        if self.__cancelling:
            self.__transferStateLock.release()
            raise Exception('S3FileStore.__startTransferOpen: cancelling')

        self.__txfer_fp = open(filePath, mode)
        self.__transferInProgress = True
        self.__transferStateLock.release()


    def __endTransfer(self):
        DEBUG('S3FileStore.__endTransfer')
        self.__transferStateLock.acquire()
        self.__txfer_fp.close()
        self.__transferInProgress = False
        self.__transferStateLock.release()


    def cancelTransfer(self):
        DEBUG('S3FileStore.cancelTransfer')
        if not self.__connected:
            raise Exception('S3FileStore.cancelTransfer: not connected')

        self.__transferStateLock.acquire()
        self.__cancelling = True
        if self.__transferInProgress:
            done = False
            count = 30
            while not done and count > 0:
                count = count - 1
                try:
                    DEBUG('S3WorkerThread.cancelTransfer: try closing fp')
                    self.__txfer_fp.close()
                    self.__transferInProgress = False
                    done = True
                    DEBUG('S3WorkerThread.cancelTransfer: done')
                except:
                    DEBUG('S3WorkerThread.cancelTransfer: bombed')
                    time.sleep(0.001)

        self.__transferStateLock.release()


    def percentCallback(self, complete, total):
        try:
            percentDone = float(complete) / total * 100
            self.__actionHandler.updateTransferProgressPercent(percentDone)
        except:
            DEBUG('S3WorkerThread.percentCallback: SetValue failed')


    def __createFolder(self, dirName):
        DEBUG('S3FileStore.__createFolder: dirName=' + dirName)
        try:
            bucket, keyName = self.getCurrentRemoteLocation()
            if not keyName.startswith('/'):
                keyName = '/' + keyName
            keyName = keyName + dirName + '/'
            k = Key(bucket)
            fileName = '.$folder$'
            k.key = keyName + fileName.replace('\\', '/')
            DEBUG('key=' + k.key)
            k.set_contents_from_string('dummy file')
            self.__dirContentsNeedsRefresh = True
            self.__actionHandler.doneAction('mkdir ' + dirName)

        except S3ResponseError as ex:
            raise Exception('S3FileStore.__createFolder: Creation of ' + dirName + ' failed: S3 error - ' + str(ex))


    def createFolder(self, dirName):
        DEBUG('S3FileStore.createFolder: dirName=' + dirName)
        if self.isCurrentFolderEncrypted():
            cryptoFolderName = self.getAndRemoveExistingCryptoDirName(dirName)
            if not cryptoFolderName:
                cryptoFolderName = self.getNewCryptoFolderName()
            self.__createFolder(cryptoFolderName)
            self.__currentFolderFolders.append(dirName)
            self.addCryptoDir(cryptoFolderName, dirName)
            self.uploadNewContentsInfo(self.__currentBucket, self.__currentDirKeys)
        else:
            self.__createFolder(dirName)


    def __normaliseLocalPath(self, localDirPath):
        DEBUG('S3FileStore.__normaliseLocalPath: localDirPath=' + localDirPath)
        if localDirPath != '.':
            localDirPath = localDirPath.replace('\\', '/')
            if len(localDirPath) > 0 and not localDirPath.endswith('/'):
                localDirPath = localDirPath + '/'
        return localDirPath


    def downloadFile(self, fileName, localDirPath='.'):
        DEBUG('S3FileStore.downloadFile: fileName=' + fileName)
        DEBUG('S3FileStore.downloadFile: localDirPath=' + localDirPath)
        try:
            tempFilePath = ''
            if not os.path.isdir(localDirPath):
                raise Exception('S3FileStore.downloadFile: dir not found ' + localDirPath)
            assert '\\' not in fileName
            assert '/' not in fileName
            self.__actionHandler.startTransfer('Downloading ' + fileName)
            if self.isCurrentFolderEncrypted():
                DEBUG('S3FileStore.downloadFile: file is encrypted')
                downloadFileName = self.getCryptoFileName(fileName)
                decrypting = True
            else:
                DEBUG('S3FileStore.downloadFile: file not encrypted')
                downloadFileName = fileName
                decrypting = False

            DEBUG('S3FileStore.downloadFile: downloadFileName = ' + downloadFileName)
            localDirPath = self.__normaliseLocalPath(localDirPath)
            downloadFilePath = downloadFileName if localDirPath == '.' else localDirPath + downloadFileName
            DEBUG('S3FileStore.downloadFile: downloadFilePath = ' + downloadFilePath)

            bucket, currentDirKey = self.getCurrentRemoteLocation()
            if currentDirKey.startswith('/'):
                currentDirKey = currentDirKey.lstrip('/')
            if len(currentDirKey) > 0 and not currentDirKey.endswith('/'):
                currentDirKey = currentDirKey + '/'
            fileKey = currentDirKey + downloadFileName.replace('\\', '/')
            DEBUG('S3FileStore.downloadFile: fileKey = ' + fileKey)
            k = bucket.get_key(fileKey)
            if not k:
                raise Exception('S3FileStore.downloadFile: file not found')

            DEBUG('S3FileStore.downloadFile: key=' + k.key)
            fileSize = k.size
            DEBUG('S3FileStore.downloadFile: fileSize=' + str(fileSize))
            tempFilePath = downloadFilePath + '.tmp'
            self.__startTransferOpen(tempFilePath, 'wb')
            k.get_contents_to_file(self.__txfer_fp, cb=self.percentCallback, num_cb=fileSize)
            self.__endTransfer()
            DEBUG('S3FileStore.downloadFile: rename ' + tempFilePath + ' to ' + downloadFilePath)
            os.rename(tempFilePath, downloadFilePath)
            tempFilePath = ''
            if decrypting:
                tmpfp = open(downloadFilePath, 'rb') # Open the local obfuscated _CFLn file we have just downloaded
                cleartextFilePath = fileName if localDirPath == '.' else localDirPath + fileName
                DEBUG('S3FileStore.downloadFile: cleartextFilePath = ' + cleartextFilePath)
                fp = open(cleartextFilePath, 'wb') # Open the file we really want to write to
                DecryptFile(tmpfp, fp, self.getEncryptionKey())
                fp.close()
                tmpfp.close()
                os.unlink(downloadFilePath)

            self.__actionHandler.endTransfer('Downloaded ' + fileName)

        except S3ResponseError as ex:
            self.__actionHandler.endTransfer('Download of ' + fileName + ' failed: S3 error - ' + str(ex))

        except Exception as ex:
            if self.__cancelling:
                self.__actionHandler.endTransfer('Cancelled download of ' + fileName)
            else:
                self.__actionHandler.endTransfer(str(ex))

        finally:
            if tempFilePath:
                try:
                    os.unlink(tempFilePath)
                except Exception as ex:
                    DEBUG('S3FileStore.downloadFile: Unlink temp file error: ' + str(ex))


    def uploadFile(self, localFilePath):
        DEBUG('S3FileStore.uploadFile: localFilePath=' + localFilePath)
        try:
            tempFilePath = ''
            plaintextFileName = ''
            if not os.path.isfile(localFilePath):
                raise Exception('S3FileStore.uploadFile: file not found ' + localFilePath)
            fileName = os.path.basename(localFilePath)
            self.__actionHandler.startTransfer('Uploading ' + fileName)
            fileSize = os.path.getsize(localFilePath)
            DEBUG('S3FileStore.uploadFile: fileName=' + fileName)
            DEBUG('S3FileStore.uploadFile: fileSize=' + str(fileSize))
            if not self.isCurrentFolderEncrypted():
                self.__startTransferOpen(localFilePath, 'rb') # If cancelled thow else set transfer in progress
                plaintextFileName = fileName
            else:
                DEBUG('S3FileStore.uploadFile: encrypt to temp file')
                sec = os.path.getmtime(localFilePath)
                timeStr = time.strftime('%Y-%m-%d %H:%M', time.localtime(sec))
                self.__startTransferOpen(localFilePath, 'rb') # If cancelled thow else set transfer in progress
                cryptoFileName = self.getAndRemoveExistingCryptoFileName(fileName)
                if not cryptoFileName:
                    cryptoFileName = self.getNewCryptoFileName()
                tempFilePath = tempfile.gettempdir() + '/' + cryptoFileName
                tmpfp = open(tempFilePath, 'wb')
                EncryptFile(self.__txfer_fp, tmpfp, self.getEncryptionKey())
                tmpfp.close() # Potential resource leak on exception
                self.__endTransfer()
                plaintextFileName = fileName
                fileName = cryptoFileName
                self.__startTransferOpen(tempFilePath, 'rb') # If cancelled thow else set transfer in progress

            DEBUG('S3FileStore.uploadFile: pos=' + str(self.__txfer_fp.tell()))
            bucket, keyName = self.getCurrentRemoteLocation()
            k = Key(bucket)
            k.key = keyName + fileName.replace('\\', '/')
            DEBUG('S3FileStore.uploadFile: key=' + k.key)
            k.set_contents_from_file(self.__txfer_fp, cb=self.percentCallback, num_cb=fileSize)
            self.__endTransfer()

            if self.isCurrentFolderEncrypted():
                self.addCryptoFile(cryptoFileName, plaintextFileName, str(fileSize), timeStr)
                self.uploadNewContentsInfo(bucket, keyName) # TODO if there's a bunch of uploads in the same folder do this once

            self.__dirContentsNeedsRefresh = True
            self.__actionHandler.endTransfer('Uploaded ' + plaintextFileName)

        except S3ResponseError as ex:
            self.__actionHandler.endTransfer('Upload of ' + plaintextFileName + ' failed: S3 error - ' + str(ex))
            
        except Exception as ex:
            if self.__cancelling:
                self.__actionHandler.endTransfer('Cancelled upload of ' + plaintextFileName)
            else:
                self.__actionHandler.endTransfer(str(ex))

        finally:
            if tempFilePath:
                try:
                    os.unlink(tempFilePath)
                except Exception as ex:
                    DEBUG('S3FileStore.uploadFile: Unlink temp file error: ' + str(ex))


    def uploadFolder(self, localFolderPath):
        DEBUG('S3FileStore.uploadFolder: localFolderPath=' + localFolderPath)
        localFolderPath = localFolderPath.replace('\\', '/')
        if not os.path.isdir(localFolderPath):
            raise Exception('S3FileStore.uploadFolder: dir not found ' + localFolderPath)
        assert not localFolderPath.endswith('/')

        lastSlashPos = localFolderPath.rfind('/')
        if lastSlashPos >= 0:
            justfolderName = localFolderPath[lastSlashPos+1:]
        else:
            justfolderName = localFolderPath
        DEBUG('S3WorkerThread.uploadFolder: justfolderName=' + justfolderName)

        originalRemoteDir = self.getCurrentRemotePath()
        self.createFolder(justfolderName)
        self.setRemoteDir(justfolderName)
        try:
            items = sorted(os.listdir(Utils.ensure_unicode(localFolderPath)))
        except Exception as ex:
            DEBUG('S3FileStore.uploadFolder: Skipping folder that I failed to read - ' + str(ex))
        else:
            for item in items:
                if self.__cancelling:
                    break;
                DEBUG('S3FileStore.uploadFolder: item=' + item)
                itemPath = localFolderPath + '/' + item
                if os.path.isdir(itemPath):
                    self.uploadFolder(itemPath)
                else:
                    self.uploadFile(itemPath)

        # Pop directory location back to parent
        self.setRemoteDir('..')
        self.__dirContentsNeedsRefresh = True
        if self.__cancelling:
            self.__actionHandler.doneAction('Cancelled upload of ' + localFolderPath)
        else:
            self.__actionHandler.doneAction('Uploaded ' + localFolderPath)


    def downloadFolder(self, folderName, localDirPath='.'):
        DEBUG('S3FileStore.downloadFolder: folderName=' + folderName)
        DEBUG('S3FileStore.downloadFolder: localDirPath=' + localDirPath)
        if not os.path.isdir(localDirPath):
            raise Exception('S3FileStore.downloadFolder: dir not found ' + localDirPath)
        assert '\\' not in folderName
        assert '/' not in folderName
        localDirPath = self.__normaliseLocalPath(localDirPath)
        downloadFolderPath = folderName if localDirPath == '.' else localDirPath + folderName
        DEBUG('S3FileStore.downloadFolder: downloadFolderPath = ' + downloadFolderPath)
        try:
            os.mkdir(downloadFolderPath)
        except OSError as ex:
            # If this is an exception because the folder or file already exists
            if 'exists' in str(ex):
                DEBUG('S3WorkerThread.__downloadFolder: merging into existing folder: ' + downloadFolderPath)
            else:
                raise Exception('S3WorkerThread.__downloadFolder: mkdir failed - ' + str(ex))

        self.setRemoteDir(folderName)
        folders, files = self.listDirsAndFiles()
        for fileEntry in files:
            if self.__cancelling:
                break;
            self.downloadFile(fileEntry[0], downloadFolderPath)
            
        for folderEntry in folders:
            if self.__cancelling:
                break;
            self.downloadFolder(folderEntry, downloadFolderPath)

        self.setRemoteDir('..')
        if self.__cancelling:
            self.__actionHandler.doneAction('Cancelled download of ' + folderName)
        else:
            self.__actionHandler.doneAction('Downloaded ' + folderName)


    def __decodeB64(self, b64):
        while len(b64) % 4 != 0:
            b64 = b64 + '='
        DEBUG('S3FileStore.DecodeB64: b64=' + b64)
        CTA_ALTCHARS = './' # const
        result = b64decode(b64, CTA_ALTCHARS)
        DEBUG('S3FileStore.DecodeB64: len(decoded result)=' + str(len(result)))
        return result


    def __generateEncryptionKey(self):
        """Use pbkdf2_sha256 to generate a hash from the password and the salt.
        The hash is used as the encryption key for the current folder.  If a
        salt has been stored already then it is re-used.
        __loadEncryptedDirContents picks up the salt from the contents
        information file: _CFCI.
        """
        # TODO move rounds to user's configuration 
        DEBUG('S3FileStore.__generateEncryptionKey')
        # If it's a new folder then we will generate a salt as well as the key.
        if len(self.__salt) > 0:
            DEBUG('S3FileStore.__generateEncryptionKey: len(salt)=' + str(len(self.__salt)))
            hashAndSalt = pbkdf2_sha256.encrypt(self.__password, salt=self.__salt, rounds=50000)
        else:
            DEBUG('S3FileStore.__generateEncryptionKey: no salt so create one')
            hashAndSalt = pbkdf2_sha256.encrypt(self.__password, salt_size=32, rounds=50000)
        DEBUG('S3FileStore.__generateEncryptionKey: hashAndSalt=' + hashAndSalt)
        # Extract and store the salt and key
        cryptoStuff = hashAndSalt.split('$')
        self.__salt = self.__decodeB64(cryptoStuff[3])
        self.__encryptionKey = self.__decodeB64(cryptoStuff[4])


    def __loadCleartextDirContents(self):
        DEBUG('S3FileStore.__loadCleartextDirContents')
        self.__currentFolderFolders = []
        self.__currentFolderFiles = []
        self.__setCurrentRemoteLocation()
        bucket, keyName = self.getCurrentRemoteLocation()
        if bucket:
            # List the folders and files
            if keyName == '/':
                keyName = ''
            try:
                files = bucket.list(keyName, '/')
            except S3ResponseError as ex:
                raise Exception('S3FileStore.__loadCleartextDirContents: directory list failed: S3 error - ' + str(ex))

            for fileEntry in files:
                DEBUG('fileEntry.name=' + fileEntry.name)
                if fileEntry.name == keyName + '.$folder$' or fileEntry.name == keyName:
                    continue

                fullName = fileEntry.name[len(keyName):]
                if fullName.endswith('/'):
                    folderName = fullName.rstrip('/')
                    self.__currentFolderFolders.append(folderName)
                else:
                    t = time.strptime(fileEntry.last_modified[:19], '%Y-%m-%dT%H:%M:%S')
                    timeStr = time.strftime('%Y-%m-%d %H:%M', t)
                    self.__currentFolderFiles.append((fullName, str(fileEntry.size), timeStr))
        else:
            # List the buckets
            buckets = self.__connection.get_all_buckets()
            for b in buckets:
                self.__currentFolderFolders.append(b.name)


    def dirtyList(self):
        DEBUG('S3FileStore.dirtyList')
        self.__dirContentsNeedsRefresh = True


    def listDirsAndFiles(self):
        DEBUG('S3FileStore.listDirsAndFiles')
        if self.__dirContentsNeedsRefresh:
            DEBUG('S3FileStore.listDirsAndFiles: refreshing dir contents')
            if self.isCurrentFolderEncrypted():
                self.__loadEncryptedDirContents()
            else:
                self.__loadCleartextDirContents()
            self.__dirContentsNeedsRefresh = False

        return self.__currentFolderFolders, self.__currentFolderFiles


    def createNewFile(self, bucket, keyName, fileName, contents):
        DEBUG('S3FileStore.createNewFile: fileName=' + fileName)
        k = Key(bucket)
        k.key = keyName + fileName.replace('\\', '/')
        DEBUG('S3FileStore.createNewFile: key=' + k.key)
        DEBUG('S3FileStore.createNewFile: contents=' + contents)
        k.set_contents_from_string(contents)


    def uploadNewContentsInfo(self, bucket, keyName):
        DEBUG('S3FileStore.uploadNewContentsInfo: len(self.__encryptionKey)=' + str(len(self.__encryptionKey)))
        if not self.__encryptionKey:
            assert not self.__salt
            self.__generateEncryptionKey()

        # Create a file called _CFCI containing list of real and crypto dir names
        dirContentsClearText = self.FOLDER_CONTENTS_HEADER + '\n' + self.__currentRemoteCryptoPath + '\n'
        for cryptoDir in self.__cryptoDirs:
            (cryptoDirName, dirName, dirSize, dirTime) = cryptoDir
            DEBUG('S3FileStore.uploadNewContentsInfo: cryptoDirName=' + cryptoDirName)
            DEBUG('S3FileStore.uploadNewContentsInfo: dirName=' + dirName)
            DEBUG('S3FileStore.uploadNewContentsInfo: dirSize=' + dirSize)
            DEBUG('S3FileStore.uploadNewContentsInfo: dirTime=' + dirTime)
            dirContentsClearText = dirContentsClearText + str(cryptoDir) + '\n'

        for cryptoFile in self.__cryptoFiles:
            (cryptoFileName, fileName, fileSize, fileTime) = cryptoFile
            DEBUG('S3FileStore.uploadNewContentsInfo: cryptoFileName=' + cryptoFileName)
            DEBUG('S3FileStore.uploadNewContentsInfo: fileName=' + fileName)
            DEBUG('S3FileStore.uploadNewContentsInfo: fileSize=' + fileSize)
            DEBUG('S3FileStore.uploadNewContentsInfo: fileTime=' + fileTime)
            dirContentsClearText = dirContentsClearText + str(cryptoFile) + '\n'

        DEBUG('S3FileStore.uploadNewContentsInfo: dirContentsClearText=' + dirContentsClearText)
        dirContentsCypherStr = EncryptStr(dirContentsClearText, self.__encryptionKey)
        DEBUG('S3FileStore.uploadNewContentsInfo: dirContentsCypherStr=' + dirContentsCypherStr)

        dirContentsStr = b64encode(self.__salt) + '\n' + dirContentsCypherStr
        DEBUG('S3FileStore.uploadNewContentsInfo: dirContentsStr=' + dirContentsStr)
        self.createNewFile(bucket, keyName, '_CFCI', dirContentsStr)


    def __loadEncryptedDirContents(self):
        """Called when we change remote folder in encrypted mode.  First we
        read the remote Cloud Filer Contents Information file called _CFCI.
        The file contains two Base64 strings separated by a newline char: the
        salt and the encrypted contents information for the current remote
        folder.  Next we generate the encryption key from the salt and the
        user's password and use it to decrypt the contents information.  We
        then check that the contents starts with the fixed header 'Nuvovis
        Cloud Filer folder contents:' and the obfuscated current remote path
        e.g.  'GC:/MySpecialBucket/_CFD0000012'.  The rest of the contents
        information is a list of directory entries in the form '(cryptoObjName,
        objName, objSize, objTime)' where cryptoObjName is the obfuscated
        folder or file name, objName is the user's folder or file name, and
        objSize and objTime are the size in bytes and timestamp of the user's
        file (zero for folders) e.g.:

        ('_CFD0000001', u'backups', '0', '0')
        ('_CFL0000003', u'py28May.tar.gz', '111064', '2018-05-28 11:39')
        
        This list is sorted by cryptoObjName and split into two lists, one for
        files and one for folders.  The next free crypto number and a free list
        of crypto numbers is also stored e.g. for the two entries above:
        
           cryptoDirs = [('_CFD0000001', u'backups', '0', '0')]
           cryptoDirHoles = []
           cryptoDirNextFree = 2
           cryptoFiles = [('_CFL0000003', u'py28May.tar.gz', '111064', '2018-05-28 11:39')]
           cryptoFileHoles = [1,2]
           cryptoFileNextFree = 4
        """
        self.__cryptoDirs = []
        self.__cryptoDirHoles = []
        self.__cryptoDirNextFree = 1
        self.__cryptoFiles = []
        self.__cryptoFileHoles = []
        self.__cryptoFileNextFree = 1
        self.__currentFolderFolders = []
        self.__currentFolderFiles = []
        try:
            self.__setCurrentRemoteLocation()
            bucket, keyName = self.getCurrentRemoteLocation()
            assert (bucket), 'no bucket'
            # Get _CFCI which is the contents information file
            fileKey = keyName + '_CFCI'
            DEBUG('S3FileStore.__loadEncryptedDirContents: download fileKey=' + fileKey)
            k = bucket.get_key(fileKey)

            # If no CFCI file found must be a new dir
            if k is None:
                DEBUG('S3FileStore.__loadEncryptedDirContents: encrypted contents file not found')
                self.uploadNewContentsInfo(bucket, keyName) # Create an empty encrypted contents file with a salt
            else:
                DEBUG('S3FileStore.__loadEncryptedDirContents: key=' + k.key)
                fileSize = k.size
                DEBUG('S3FileStore.__loadEncryptedDirContents: fileSize=' + str(fileSize))
                folderContentsSaltAndCypherStr = k.get_contents_as_string()
                DEBUG('S3FileStore.__loadEncryptedDirContents: folderContentsSaltAndCypherStr=' + folderContentsSaltAndCypherStr)

                # Split salt from cypher
                ciBits = folderContentsSaltAndCypherStr.split('\n', 1)
                b64salt = ciBits[0]
                folderContentsCypherStr = ciBits[1]

                # Generate the encryption key from the password and the salt
                DEBUG('S3FileStore.__loadEncryptedDirContents: b64salt=' + b64salt)
                remoteSalt = b64decode(b64salt)
                self.__salt = remoteSalt
                self.__generateEncryptionKey()

                try:
                    DEBUG('S3FileStore.__loadEncryptedDirContents: folderContentsCypherStr=' + folderContentsCypherStr)
                    contentsListStr = DecryptStr(folderContentsCypherStr, self.__encryptionKey)
                    DEBUG('S3FileStore.__loadEncryptedDirContents: contentsListStr=' + contentsListStr)

                    # Check the contents info decrypted ok
                    contentsList = contentsListStr.split('\n')
                    if contentsList[0] != self.FOLDER_CONTENTS_HEADER:
                        raise Exception('S3FileStore.__loadEncryptedDirContents: failed to decrypt - ' + contentsList[0])

                except Exception as ex:
                    DEBUG('S3FileStore.__loadEncryptedDirContents: decryption ex: ' + str(ex))
                    raise Exception('S3FileStore.__loadEncryptedDirContents: failed to decrypt')

                DEBUG('S3FileStore.__loadEncryptedDirContents: currentRemoteCryptoPath=' + self.__currentRemoteCryptoPath)
                if self.__currentRemoteCryptoPath != contentsList[1]:
                    raise Exception('S3FileStore.__loadEncryptedDirContents: Crypto path mismatch: expected ' + self.__currentRemoteCryptoPath + ' found ' + contentsList[1])

                remoteObjList = []
                for obj in contentsList[2:]:
                    DEBUG('S3FileStore.__loadEncryptedDirContents: obj=' + obj)
                    if obj: # There may be a blank line at the end
                        remoteObjList.append(literal_eval(obj)) # (cryptoObjName, objName, objSize, objTime)

                # Sort the remote list by crypto name so we can work out holes we can reuse and discard duplicate entries
                remoteObjList = sorted(remoteObjList, key=lambda (s1, s2, s3, s4): s1)

                expectedNextDirNumber = 1
                expectedNextFileNumber = 1
                for remoteObj in remoteObjList:
                    (cryptoObjName, objName, objSize, objTime) = remoteObj
                    DEBUG('S3FileStore.__loadEncryptedDirContents: cryptoObjName=' + cryptoObjName)
                    DEBUG('S3FileStore.__loadEncryptedDirContents: objName=' + objName)
                    DEBUG('S3FileStore.__loadEncryptedDirContents: objSize=' + objSize)
                    DEBUG('S3FileStore.__loadEncryptedDirContents: objTime=' + objTime)
                    objNumber = int(cryptoObjName[4:])
                    if cryptoObjName.startswith('_CFD'):
                        DEBUG('S3FileStore.__loadEncryptedDirContents: found a dir')
                        while objNumber > expectedNextDirNumber:
                            DEBUG('S3FileStore.__loadEncryptedDirContents: found a hole: ' + str(expectedNextDirNumber))
                            self.__cryptoDirHoles.append(expectedNextDirNumber)
                            expectedNextDirNumber = expectedNextDirNumber + 1

                        if objNumber != expectedNextDirNumber:
                            raise Exception('S3FileStore.__loadEncryptedDirContents: Duplicate remote dir ref discarded: cryptoObjName=' + cryptoObjName)
                        else:
                            self.addCryptoDir(cryptoObjName, objName)
                            self.__currentFolderFolders.append(objName)
                            expectedNextDirNumber = objNumber + 1

                    elif cryptoObjName.startswith('_CFL'):
                        DEBUG('S3FileStore.__loadEncryptedDirContents: found a file')
                        while objNumber > expectedNextFileNumber:
                            DEBUG('S3FileStore.__loadEncryptedDirContents: found a hole: ' + str(expectedNextFileNumber))
                            self.__cryptoFileHoles.append(expectedNextFileNumber)
                            expectedNextFileNumber = expectedNextFileNumber + 1

                        if objNumber != expectedNextFileNumber:
                            raise Exception('S3FileStore.__loadEncryptedDirContents: Duplicate remote file ref discarded: cryptoObjName=' + cryptoObjName)
                        else:
                            self.addCryptoFile(cryptoObjName, objName, objSize, objTime)
                            self.__currentFolderFiles.append((objName, str(objSize), objTime))
                            expectedNextFileNumber = objNumber + 1
                    else:
                        raise Exception('S3FileStore.__loadEncryptedDirContents: Found a WTF: cryptoObjName=' + cryptoObjName + ' objName=' + objName)

                self.__cryptoDirNextFree = expectedNextDirNumber
                self.__cryptoFileNextFree = expectedNextFileNumber

        except S3ResponseError as ex:
            msg = ex.error_message if ex.error_message else str(ex)
            raise Exception('S3FileStore.__loadEncryptedDirContents: S3 Error (getting encrypted dir contents): "' + msg + '"')

        except Exception as ex:
            raise Exception('S3FileStore.__loadEncryptedDirContents: Error (getting encrypted dir contents): ' + str(ex))


    def getCryptoFileName(self, cleartextFileName):
        DEBUG('getCryptoFileName: cleartextFileName=' + cleartextFileName)
        fileNameList = filter(lambda (s1, s2, s3, s4): s2 == cleartextFileName, self.__cryptoFiles)
        if len(fileNameList) == 1:
            (s1, s2, s3, s4) = fileNameList[0]
            DEBUG('getCryptoFileName: found ' + s1)
            return s1
        else:
            raise Exception('getCryptoFileName ' + cleartextFileName + ' found ' + str(len(fileNameList)) + ' entries')


    def getCryptoFolderName(self, cleartextDirName):
        """Converts the cleartext folder name to a crypto folder name like
        _CFD00005 by looking it up in self.__cryptoDirs.
        """
        DEBUG('S3FileStore.getCryptoFolderName: cleartextDirName=' + cleartextDirName)
        dirNameList = filter(lambda (s1, s2, s3, s4): s2 == cleartextDirName, self.__cryptoDirs)
        if len(dirNameList) == 1:
            (s1, s2, s3, s4) = dirNameList[0]
            DEBUG('S3FileStore.getCryptoFolderName: found ' + s1)
            return s1
        else:
            raise Exception('S3FileStore.getCryptoFolderName: for ' + cleartextDirName + ' found ' + str(len(dirNameList)) + ' entries')


