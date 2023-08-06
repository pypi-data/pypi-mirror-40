# FileListCtrl
#
# Inherits from wx.ListCtrl and shows a list of folders and files.  Cloud Filer
# has two FileListCtrls: one top left showing the local files and one top right
# showing the remote files.  The remote FileListCtrl has an S2FileStore which
# is used to keep track of the remote folder location and provides the list of
# folders and files.  The local FileListCtrl uses the os.path functions to move
# the current working directory and list local folders and files.
#
# Both FileListCtrls have a reference to the shared job queue used to enqueue
# S3 worker jobs: uploads, downloads and deletes.
#
import sys
import os
import wx
import time
import re
import Utils
import S3WorkerThread

from Utils import DEBUG
from S3WorkerThread import S3Job
from S3WorkerThread import TransferJobData
from S3WorkerThread import S3EVT_TXDONE
from S3FileStore import S3FileStore
from NewFolderDlg import NewFolderDlg

SORT_BY_FILENAME = 0
SORT_BY_FILESIZE = 1
SORT_BY_FILETYPE = 2
SORT_BY_MODIFIED = 3


class FileListCtrl(wx.ListCtrl):

    def __init__(self, *args, **kwargs):
        super(FileListCtrl, self).__init__(*args, **kwargs) 
        self.__connected = False
        self.InitUI()
     

    def InitUI(self):
        S3EVT_TXDONE(self, self.OnViewRefresh)

        self.InsertColumn(0, 'Name', width = 270)
        self.InsertColumn(1, 'Size', width = 100)
        self.InsertColumn(2, 'Type', width = 100)
        self.InsertColumn(3, 'Modified', width = 120)

        self.il = wx.ImageList(16, 16)
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_UP_DIR)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_FOLDER)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_DOC_PLAIN)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_LOCK)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_DOC_TEXT)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_DOC_PDF)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_DOC_IMAGE)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_PACKAGE)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_MUSIC)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_FILM)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_SUBTITLES)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_CDROM)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_SCRIPT_PYTHON)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_DOC_WORD)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_DOC_EXCEL)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_DOC_POWERPOINT)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_DOC_HTML)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_SIGNATURE)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_REMOTE_FOLDER)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_CSS)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_SCRIPT)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_EXE)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_LIB)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_DLL)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_SMALL_ARROW_DOWN)))
        self.il.Add(wx.Bitmap(Utils.GetFilePath(Utils.ICON_SMALL_ARROW_UP)))

        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

        self.__sortAscending = True
        self.sortColumn = SORT_BY_FILENAME
        self.SwitchOnSortIndicator()

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.DoubleClick)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColumnClick)


    def Init(self, queue, remoteIcon, comboBox, outputList, rdl):
        self.__queue = queue
        self.__remoteIcon = remoteIcon
        self.__combo = comboBox
        self.__outputList = outputList
        self.__remoteDirList = rdl


    def S3Connect(self, accessKey, secretKey, password, proxyServer, proxyUsername, proxyPassword, cloudService, cloudHost, cloudRootText):
        try:
            self.__outputList.Append('Connecting to ' + cloudService + '...')
            self.__combo.Clear()
            self.__combo.SetValue('')
            self.__S3FS = S3FileStore(self.__outputList)
            self.__connection = self.__S3FS.connect(accessKey, secretKey, password, cloudHost, cloudRootText)
            self.DeleteAllItems() # I am a ListCtrl and should be emptied
            self.__outputList.Append('Connected')
            self.__cloudRootText = cloudRootText
            if len(password) > 0:
                self.SetBackgroundColour(wx.Colour(200,240,200))
                self.__remoteIcon.SetBitmap(wx.Bitmap(Utils.GetFilePath(Utils.ICON_GREEN_SHIELD)))
            else:
                self.SetBackgroundColour(wx.Colour(255,255,255))
                self.__remoteIcon.SetBitmap(wx.Bitmap(Utils.GetFilePath(Utils.ICON_RED_SHIELD)))

            self.__connected = True
            return self.__connection

        except Exception as ex:
            errorMessage = str(ex)
            self.__outputList.Append('Error: ' + errorMessage)


    def IsConnected(self):
        return self.__connected


    def OnViewRefresh(self, e):
        # If this is the remote list
        if self.__remoteDirList == None:
            self.RefreshRemoteDir()
        else:
            self.RefreshDir()


    def SwitchOffSortIndicator(self):
        self.ClearColumnImage(self.sortColumn)


    def SwitchOnSortIndicator(self):
        if self.__sortAscending:
            self.SetColumnImage(self.sortColumn, Utils.ICON_SMALL_ARROW_DOWN)
        else:
            self.SetColumnImage(self.sortColumn, Utils.ICON_SMALL_ARROW_UP)


    def ResetColumnSorting(self):
        self.SwitchOffSortIndicator()
        self.__sortAscending = True
        self.sortColumn = SORT_BY_FILENAME
        self.SwitchOnSortIndicator()


    def OnColumnClick(self, e):
        DEBUG('OnColumnClick: ' + str(e.GetColumn()))
        self.DeleteAllItems()
        # if user clicked on the current column
        if e.GetColumn() == self.sortColumn:
            # Toggle sort order and change title
            if self.__sortAscending:
                self.__sortAscending = False
            else:
                self.__sortAscending = True
            self.SwitchOnSortIndicator()

        else:
            self.SwitchOffSortIndicator()
            # Switch back to normal ascending sort
            self.__sortAscending = True
            # Set new sort column
            self.sortColumn = e.GetColumn()
            self.SwitchOnSortIndicator()

        self.DisplayFileList()


    def CanUpload(self):
        return self.__connected and not self.__S3FS.isCurrentFolderRoot()


    def OnRightDown(self, e):
        DEBUG('OnRightDown')
        try:
            # If have selected a single folder or bucklet then add Open action
            fileName = ''
            self.menu = wx.Menu()
            mi = wx.MenuItem(self.menu, wx.NewId(), 'Refresh')
            self.menu.AppendItem(mi)
            self.Bind(wx.EVT_MENU, self.OnViewRefresh, mi)
            if self.GetSelectedItemCount() == 1:
                fileName = self.GetItem(self.GetFirstSelected(), 0).GetText()
                fileType = self.GetItem(self.GetFirstSelected(), 2).GetText()
                DEBUG('fileName=' + fileName)
                DEBUG('fileType=' + fileType)
                if (fileType == 'Folder' or fileType == 'Bucket'):
                    mi = wx.MenuItem(self.menu, wx.NewId(), 'Open')
                    self.menu.AppendItem(mi)
                    self.Bind(wx.EVT_MENU, self.DoubleClick, mi)

            # If this is the remote list
            if self.__remoteDirList == None:
                DEBUG('Remote') 
                # If we are connected
                if self.__connected:
                    if self.menu.GetMenuItemCount() > 0:
                        self.menu.AppendSeparator()

                    # If not at root showing bucket list
                    if not self.__S3FS.isCurrentFolderRoot():
                        if self.GetSelectedItemCount() == 1:
                            fileType = self.GetItem(self.GetFirstSelected(), 2).GetText()
                            DEBUG('fileType=' + fileType)

                        mi = wx.MenuItem(self.menu, wx.NewId(), 'New Folder')
                        self.menu.AppendItem(mi)
                        self.Bind(wx.EVT_MENU, self.OnNewFolder, mi)
                        if self.GetSelectedItemCount() > 0:
                            mi = wx.MenuItem(self.menu, wx.NewId(), 'Delete')
                            self.menu.AppendItem(mi)
                            self.Bind(wx.EVT_MENU, self.OnDelete, mi)
                            self.menu.AppendSeparator()
                            mi = wx.MenuItem(self.menu, wx.NewId(), 'Download')
                            self.menu.AppendItem(mi)
                            self.Bind(wx.EVT_MENU, self.OnDownload, mi)
            else:
                DEBUG('Local') 
                # If something is selected
                if self.GetSelectedItemCount() > 0:
                    # If the remote side can accept stuff and the up dir (always first) is not selected
                    if self.__remoteDirList.CanUpload() and self.GetItemText(self.GetFirstSelected()) != '..':
                        if self.menu.GetMenuItemCount() > 0:
                            self.menu.AppendSeparator()

                        mi = wx.MenuItem(self.menu, wx.NewId(), 'Upload')
                        self.menu.AppendItem(mi)
                        self.Bind(wx.EVT_MENU, self.OnUpload, mi)

            if self.menu.GetMenuItemCount() > 0:
                self.PopupMenu(self.menu, e.GetPosition())

        except Exception as ex:
            errorMessage = str(ex)
            self.__outputList.Append('Error: ' + errorMessage)


    def GetCurrentRemotePath(self):
        return self.__S3FS.getCurrentRemotePath()


    def DirtyList(self):
        self.__S3FS.dirtyList()


    def DoTransfer(self, isDownload):
        currentItem = self.GetFirstSelected()
        while currentItem != -1:
            name = self.GetItem(currentItem, 0).GetText()
            fileType = self.GetItem(currentItem, 2).GetText()
            DEBUG('name=' + name)
            DEBUG('fileType=' + fileType)
#            if name.startswith('_CF'):
#                self.__outputList.Append('Skipping file that looks like a CloudFiler encrypted item: ' + name)
#                continue

            if fileType == 'Folder':
                if isDownload:
                    self.__queue.put(S3Job(S3WorkerThread.JOB_TYPE_DOWNLOAD, TransferJobData(True, os.getcwd(), self.__S3FS.getCurrentRemotePath(), name)))
                    self.__outputList.Append('Queued download of folder ' + name)
                else:
                    self.__queue.put(S3Job(S3WorkerThread.JOB_TYPE_UPLOAD, TransferJobData(True, os.getcwd(), self.__remoteDirList.GetCurrentRemotePath(), name)))
                    self.__outputList.Append('Queued upload of folder ' + name)
                    self.__remoteDirList.DirtyList()
            else:
                if isDownload:
                    self.__queue.put(S3Job(S3WorkerThread.JOB_TYPE_DOWNLOAD, TransferJobData(False, os.getcwd(), self.__S3FS.getCurrentRemotePath(), name)))
                    self.__outputList.Append('Queued download of file ' + name)
                else:
                    self.__queue.put(S3Job(S3WorkerThread.JOB_TYPE_UPLOAD, TransferJobData(False, os.getcwd(), self.__remoteDirList.GetCurrentRemotePath(), name)))
                    self.__outputList.Append('Queued upload of file ' + name)
                    self.__remoteDirList.DirtyList()

            currentItem = self.GetNextSelected(currentItem)

        if isDownload:
            self.__queue.put(S3Job(S3WorkerThread.JOB_TYPE_DOWNLOAD_END, None))
        else:
            self.__queue.put(S3Job(S3WorkerThread.JOB_TYPE_UPLOAD_OR_DELETE_END, None))


    def OnUpload(self, e):
        self.DoTransfer(False)
            

    def OnDownload(self, e):
        """Called when either the right-click menu Download action is clicked
        or when the Transfer-Download menu is clicked.  Before the user starts
        the download they select some files and/or folders in the right hand
        remote file list and the selected items are then downloaded.  Iterates
        over the selected items and foreach item adds a download job to the
        worker queue.
        """
        self.DoTransfer(True)


    def OnNewFolder(self, e):
        dlg = NewFolderDlg(self, wx.ID_ANY, 'Create new folder')
        if dlg.ShowModal() == wx.ID_OK:
            self.__S3FS.createFolder(dlg.GetName()) 

        dlg.Destroy()
        self.RefreshRemoteDir()


    def OnDelete(self, e):
        prompt = True
        currentItem = self.GetFirstSelected()
        while currentItem != -1:
            name = self.GetItem(currentItem, 0).GetText()
            itemType = self.GetItem(currentItem, 2).GetText()
            showApplyToAll = False
            if itemType == 'Folder':
                action = Utils.ACTION_DELETE_FOLDER
            else:
                action = Utils.ACTION_DELETE_FILE
            if prompt:
                if self.GetSelectedItemCount() > 1:
                    showApplyToAll = True
                dlg = Utils.WarningDlg(action, showApplyToAll, name, self, wx.ID_ANY, 'Cloud Filer - Warning')
                dlg.ShowModal()
                status = dlg.GetEndId()
                dlg.Destroy()
            if status == wx.ID_OK:
                if showApplyToAll and dlg.GetApplyAll():
                    prompt = False

                self.__queue.put(S3Job(S3WorkerThread.JOB_TYPE_DELETE, TransferJobData(action == Utils.ACTION_DELETE_FOLDER, '', self.__S3FS.getCurrentRemotePath(), name)))
                self.__outputList.Append('Queued delete of ' + name)
                self.DirtyList()

            currentItem = self.GetNextSelected(currentItem)

        self.__queue.put(S3Job(S3WorkerThread.JOB_TYPE_UPLOAD_OR_DELETE_END, None))
        

    def DoubleClick(self, event):
        if self.GetSelectedItemCount() == 1:
            fileName = self.GetItem(self.GetFirstSelected(), 0).GetText()
            fileType = self.GetItem(self.GetFirstSelected(), 2).GetText()
            DEBUG('fileName=' + fileName)
            DEBUG('fileType=' + fileType)
            if fileType == 'Folder' or fileType == 'Bucket':
                DEBUG('it is a folder')
                if self.__connected:
                    self.ChangeRemoteDir(fileName)
                else:
                    # Try to do local cd
                    if (self.SetDir(fileName)):
                        cwd = os.getcwd()
                        if self.__combo.FindString(cwd) == wx.NOT_FOUND:
                            self.__combo.Append(cwd)

                        self.__combo.SetStringSelection(cwd)
            else:
                DEBUG('not a folder')


    def WindowsRootDir(self, pathStr):
        return len(pathStr) == 3 and re.match(r'[A-Z]:\\', pathStr)


    def SetDir(self, dirPath):
        DEBUG('SetDir: ' + dirPath)
        try:
            os.chdir(dirPath)
        except OSError:
            return False

        self.DeleteAllItems()
        self.__outputList.Append('lcd ' + dirPath)
        items = os.listdir(u'.')
        self.currentFolderFolders = []
        self.currentFolderFiles = []
        # Add folders
        for folder in filter(lambda i: os.path.isdir(i), items):
            #TODO also filter fnmatch.fnmatch(i, __ignore_pattern):

            # Skip any folder we can't access
            try:
                os.listdir(Utils.ensure_unicode(folder))
            except Exception as ex:
                errorMessage = str(ex)
                DEBUG('Error: ' + errorMessage)
                continue  

            size = os.path.getsize(folder)
            sec = os.path.getmtime(folder)
            timeStr = time.strftime('%Y-%m-%d %H:%M', time.localtime(sec))
            self.currentFolderFolders.append((folder, '', 'Folder', timeStr, 1))

        # Add files
        for f in filter(lambda i: not os.path.isdir(i), items):
            try:
                size = os.path.getsize(f)
                sec = os.path.getmtime(f)
                timeStr = time.strftime('%Y-%m-%d %H:%M', time.localtime(sec))
                self.AddFileToCurrentFolderList(f, str(size), timeStr)
            except Exception as ex:
                errorMessage = str(ex)
                self.__outputList.Append('Error: ' + errorMessage)
                continue  

        self.ResetColumnSorting()
        self.DisplayFileList()
        return True


    def RefreshDir(self):
        self.SetDir(os.getcwd())


    def GetFileType(self, ex):
        if (ex == 'gpg' or ex == 'pgp'):
            fileType = 'Encrypted'
            imageIndex = 3
        elif (ex == 'tc'):
            fileType = 'TrueCrypt'
            imageIndex = 3
        elif (ex == 'txt' or ex == 'log'):
            fileType = 'Text'
            imageIndex = 4
        elif (ex == 'nfo'):
            fileType = 'Info'
            imageIndex = 4
        elif (ex == 'pdf'):
            fileType = 'Document'
            imageIndex = 5
        elif (ex == 'png' or ex == 'jpg' or ex == 'bmp' or ex == 'gif'):
            fileType = 'Image'
            imageIndex = 6
        elif (ex == 'tgz' or ex == 'gz' or ex == 'zip' or ex == 'tar' or ex == 'rar' or ex == 'msi' or ex == 'msp'):
            fileType = 'Archive'
            imageIndex = 7
        elif (ex == 'wav' or ex == 'mp3' or ex == 'm4a'):
            fileType = 'Audio'
            imageIndex = 8
        elif (ex == 'avi' or ex == 'mpg' or ex == 'mp4' or ex == 'ogm' or ex =='flv'):
            fileType = 'Video'
            imageIndex = 9
        elif (ex == 'idx' or ex == 'sub' or ex == 'srt'):
            fileType = 'Subtitles'
            imageIndex = 10
        elif (ex == 'iso'):
            fileType = 'Disk Image'
            imageIndex = 11
        elif (ex == 'py'):
            fileType = 'Text'
            imageIndex = 12
        elif (ex == 'odt' or ex == 'doc' or ex == 'docx' or ex == 'docm'):
            fileType = 'Document'
            imageIndex = 13
        elif (ex == 'ods' or ex == 'xls' or ex == 'xlsx' or ex == 'xlsm'):
            fileType = 'Spreadsheet'
            imageIndex = 14
        elif (ex == 'odp' or ex == 'ppt' or ex == 'pptx' or ex == 'pptm' or ex == 'ppsx' or ex == 'ppsm'):
            fileType = 'Presentation'
            imageIndex = 15
        elif (ex == 'odg' or ex == 'dia' or ex == 'vsd' or ex == 'vdx' or ex == 'vsx' or ex == 'vss'):
            fileType = 'Diagram'
            imageIndex = 6
        elif (ex == 'htm' or ex == 'html'):
            fileType = 'Web Page'
            imageIndex = 16
        elif (ex == 'sig' or ex == 'asc'):
            fileType = 'Signature'
            imageIndex = 17
        elif (ex == 'css'):
            fileType = 'Style Sheet'
            imageIndex = Utils.ICON_CSS
        elif (ex == 'js' or ex == 'sh' or ex == 'vbs' or ex == 'pl' or ex == 'ps2' or ex == 'ps1' or ex == 'bat' or ex == 'jse' or ex == 'reg' or ex == 'vb'):
            fileType = 'Script'
            imageIndex = Utils.ICON_SCRIPT
        elif (ex == 'exe'):
            fileType = 'Executable'
            imageIndex = Utils.ICON_EXE
        elif (ex == 'dll' or ex == 'so'):
            fileType = 'Dynamic Library'
            imageIndex = Utils.ICON_DLL
        elif (ex == 'lib' or ex == 'a'):
            fileType = 'Static Library'
            imageIndex = Utils.ICON_LIB
        else:
            fileType = ''
            imageIndex = 2

        return (fileType, imageIndex)


    def RefreshRemoteDir(self):
        self.DisplayRemoteFolder()


    def ChangeRemoteDir(self, newDir):
        DEBUG('ChangeRemoteDir: newDir=' + newDir)
        before = self.__S3FS.getCurrentRemotePath()
        try:
            self.__S3FS.setRemoteDir(newDir)
            self.DisplayRemoteFolder()

            cwd = self.__S3FS.getCurrentRemotePath()
            if self.__combo.FindString(cwd) == wx.NOT_FOUND:
                self.__combo.Append(cwd)
            self.__combo.SetStringSelection(cwd)
        except Exception as ex:
            self.__outputList.Append('Error: ' + str(ex))
            self.__S3FS.setRemoteDir(before)
            self.DisplayRemoteFolder()


    def AddFileToCurrentFolderList(self, fullName, fileSize, timeStr):
        if '.' in fullName:
            dotIdx = fullName.rfind('.')
            ext = fullName[dotIdx+1:].lower()
        else:
            ext = ''
        fileType, imageIndex = self.GetFileType(ext)
        self.currentFolderFiles.append((fullName, fileSize, fileType, timeStr, imageIndex))


    def DisplayRemoteFolder(self):
        DEBUG('Display folder')
        self.DeleteAllItems()
        self.currentFolderFolders = []
        self.currentFolderFiles = []
        if self.__connected:
            dirs, files = self.__S3FS.listDirsAndFiles()
            for d in dirs:
                self.currentFolderFolders.append((d, '', 'Folder', '', 1))
            for f in files:
                self.AddFileToCurrentFolderList(f[0], f[1], f[2])

            self.ResetColumnSorting()

        self.DisplayFileList()
               

    def AtRoot(self):
        # If this is the local file list
        if self.__remoteDirList:
            return os.getcwd() == '/' or self.WindowsRootDir(os.getcwd())
        else:
            return not self.__connected or self.__S3FS.isCurrentFolderRoot()


    def DisplayFileList(self):
        if self.sortColumn == SORT_BY_FILENAME:
            # sort by filename
            if self.__sortAscending:
                self.currentFolderFolders = sorted(self.currentFolderFolders, key=lambda (s1, s2, s3, s4, i1): s1.lower())
                self.currentFolderFiles = sorted(self.currentFolderFiles, key=lambda (s1, s2, s3, s4, i1): s1.lower())
            else:
                self.currentFolderFolders = sorted(self.currentFolderFolders, key=lambda (s1, s2, s3, s4, i1): s1.lower(), reverse=True)
                self.currentFolderFiles = sorted(self.currentFolderFiles, key=lambda (s1, s2, s3, s4, i1): s1.lower(), reverse=True)
        elif self.sortColumn == SORT_BY_FILESIZE:
            # sort by filesize
            if self.__sortAscending:
                self.currentFolderFolders = sorted(self.currentFolderFolders, key=lambda (s1, s2, s3, s4, i1): s1.lower())
                self.currentFolderFiles = sorted(self.currentFolderFiles, key=lambda (s1, s2, s3, s4, i1): int(s2))
            else:
                self.currentFolderFolders = sorted(self.currentFolderFolders, key=lambda (s1, s2, s3, s4, i1): s1.lower())
                self.currentFolderFiles = sorted(self.currentFolderFiles, key=lambda (s1, s2, s3, s4, i1): int(s2), reverse=True)
        elif self.sortColumn == SORT_BY_FILETYPE:
            # sort by filetype
            if self.__sortAscending:
                self.currentFolderFolders = sorted(self.currentFolderFolders, key=lambda (s1, s2, s3, s4, i1): s1.lower())
                self.currentFolderFiles = sorted(self.currentFolderFiles, key=lambda (s1, s2, s3, s4, i1): s3.lower())
            else:
                self.currentFolderFolders = sorted(self.currentFolderFolders, key=lambda (s1, s2, s3, s4, i1): s1.lower())
                self.currentFolderFiles = sorted(self.currentFolderFiles, key=lambda (s1, s2, s3, s4, i1): s3.lower(), reverse=True)
        elif self.sortColumn == SORT_BY_MODIFIED:
            # sort by modification timestamp
            if self.__sortAscending:
                self.currentFolderFolders = sorted(self.currentFolderFolders, key=lambda (s1, s2, s3, s4, i1): s4)
                self.currentFolderFiles = sorted(self.currentFolderFiles, key=lambda (s1, s2, s3, s4, i1): s4)
            else:
                self.currentFolderFolders = sorted(self.currentFolderFolders, key=lambda (s1, s2, s3, s4, i1): s4, reverse=True)
                self.currentFolderFiles = sorted(self.currentFolderFiles, key=lambda (s1, s2, s3, s4, i1): s4, reverse=True)

        if not self.AtRoot():
            index = self.InsertStringItem(sys.maxint, '..')
            self.SetStringItem(index, 2, 'Folder')
            self.SetItemImage(index, 0)

        for details in self.currentFolderFolders:
            index = self.InsertStringItem(sys.maxint, details[0])
            self.SetStringItem(index, 1, details[1])
            self.SetStringItem(index, 2, details[2])
            self.SetStringItem(index, 3, details[3])
            self.SetItemImage(index, details[4])

        for details in self.currentFolderFiles:
            index = self.InsertStringItem(sys.maxint, details[0])
            self.SetStringItem(index, 1, details[1])
            self.SetStringItem(index, 2, details[2])
            self.SetStringItem(index, 3, details[3])
            self.SetItemImage(index, details[4])


