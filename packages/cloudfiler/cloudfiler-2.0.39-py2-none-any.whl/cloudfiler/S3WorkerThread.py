# S3WorkerThread
#
# Three S3 actions can take some time and so are passed on by the main GUI
# thread to this worker thread object: uploads, downloads and remote deletions.
#
import os
import wx
import threading
import traceback

from Utils import DEBUG
from S3FileStore import S3FileStore


JOB_TYPE_DOWNLOAD = 1
JOB_TYPE_DOWNLOAD_END = 2
JOB_TYPE_UPLOAD = 3
JOB_TYPE_UPLOAD_OR_DELETE_END = 4
JOB_TYPE_DELETE = 5


ID_S3EVT_ACTION = wx.NewId()
def S3EVT_ACTION(win, func):
    win.Connect(-1, -1, ID_S3EVT_ACTION, func)


class ActionEvent(wx.PyEvent):
    """Event used to communicate back the status of an action such as a
    download action: e.g. start of action, progress or end.
    """
    def __init__(self, actionID, actionStr):
        wx.PyEvent.__init__(self)
        self.SetEventType(ID_S3EVT_ACTION)
        self.actionID = actionID # 1 - Start; 2 - Progress; 3 - End
        self.actionStr = actionStr


ID_S3EVT_TXDONE = wx.NewId()
def S3EVT_TXDONE(win, func):
    win.Connect(-1, -1, ID_S3EVT_TXDONE, func)


class TransferFinishedEvent(wx.PyEvent):
    def __init__(self):
        wx.PyEvent.__init__(self)
        self.SetEventType(ID_S3EVT_TXDONE)


class S3Job:
    """Generic job object containing a job type tag and a data payload.
    """
    def __init__(self, jobType, jobData):
        self.jobType = jobType
        self.jobData = jobData


class TransferJobData:
    def __init__(self, isFolder, currentLocalPath, currentRemotePath, name):
        self.isFolder = isFolder
        self.localPath = currentLocalPath
        self.remotePath = currentRemotePath
        self.name = name


class S3WorkerThread (threading.Thread):

    def __init__(self, workQueue, localFileList, remoteFileList, outputList):
        threading.Thread.__init__(self)
        self.__workQueue = workQueue
        self.__localFileList = localFileList
        self.__remoteFileList = remoteFileList
        self.__outputList = outputList
        self.__wantAbort = False
        self.__S3FS = S3FileStore(self)


    def startTransfer(self, msg):
        wx.PostEvent(self.__outputList, ActionEvent(1, msg))


    def endTransfer(self, msg):
        wx.PostEvent(self.__outputList, ActionEvent(3, msg))


    def doneAction(self, msg):
        wx.PostEvent(self.__outputList, ActionEvent(4, msg))


    def updateTransferProgressPercent(self, percentDone):
        wx.PostEvent(self.__outputList, ActionEvent(2, percentDone))


    def setConnection(self, connection, cloudRootText, password):
        DEBUG('S3WorkerThread.setConnection: cloudRootText=' + cloudRootText)
        self.__S3FS.setConnection(connection, cloudRootText, password)
        
        
    def abort(self):
        try:
            if not self.__workQueue.empty():
                self.__wantAbort = True
            self.__S3FS.cancelTransfer()

        except Exception as ex:
            DEBUG(str(ex))
            traceback.print_exc()
            self.doneAction(str(ex))


    def __download(self, isFolder, name, targetPath):
        DEBUG('S3WorkerThread.__download: isFolder=' + str(isFolder))
        DEBUG('S3WorkerThread.__download: name=' + name)
        DEBUG('S3WorkerThread.__download: targetPath=' + targetPath)
        if isFolder:
            self.__S3FS.downloadFolder(name, targetPath)
        else:
            self.__S3FS.downloadFile(name, targetPath)


    def __upload(self, isFolder, name, sourcePath):
        DEBUG('S3WorkerThread.__upload: isFolder=' + str(isFolder))
        DEBUG('S3WorkerThread.__upload: name=' + name)
        DEBUG('S3WorkerThread.__upload: targetPath=' + sourcePath)
        path = sourcePath + '/' + name
        DEBUG('S3WorkerThread.__upload: path=' + path)
        if isFolder:
            self.__S3FS.uploadFolder(path)
        else:
            self.__S3FS.uploadFile(path)


    def __runJob(self, job):
        try:
            DEBUG('S3WorkerThread.__runJob')
            if self.__wantAbort:
                DEBUG('S3WorkerThread.__runJob: abort set; skipping job')
                return

            if job.jobType == JOB_TYPE_DOWNLOAD:
                DEBUG('S3WorkerThread.__runJob: download job - remotePath=' + job.jobData.remotePath)
                self.__S3FS.setRemoteDir(job.jobData.remotePath)
                DEBUG('S3WorkerThread.__runJob: job.jobData.name=' + job.jobData.name)
                self.__download(job.jobData.isFolder, job.jobData.name, job.jobData.localPath)
            elif job.jobType == JOB_TYPE_DOWNLOAD_END:
                DEBUG('S3WorkerThread.__runJob: download batch done job')
                wx.PostEvent(self.__localFileList, TransferFinishedEvent())
            elif job.jobType == JOB_TYPE_UPLOAD:
                DEBUG('S3WorkerThread.__runJob: upload job - remotePath=' + job.jobData.remotePath)
                self.__S3FS.setRemoteDir(job.jobData.remotePath)
                DEBUG('S3WorkerThread.__runJob: job.jobData.name=' + job.jobData.name)
                self.__upload(job.jobData.isFolder, job.jobData.name, job.jobData.localPath)
            elif job.jobType == JOB_TYPE_DELETE:
                DEBUG('S3WorkerThread.__runJob: delete job - remotePath=' + job.jobData.remotePath)
                self.__S3FS.setRemoteDir(job.jobData.remotePath)
                DEBUG('S3WorkerThread.__runJob: job.jobData.name=' + job.jobData.name)
                if job.jobData.isFolder:
                    self.__S3FS.deleteFolder(job.jobData.name)
                else:
                    self.__S3FS.deleteFile(job.jobData.name)
            elif job.jobType == JOB_TYPE_UPLOAD_OR_DELETE_END:
                DEBUG('S3WorkerThread.__runJob: upload or delete batch done job')
                wx.PostEvent(self.__remoteFileList, TransferFinishedEvent())
            else:
                DEBUG('S3WorkerThread.__runJob: TODO')

        except Exception as ex:
            DEBUG(str(ex))
            traceback.print_exc()
            self.doneAction(str(ex))


    def run(self):
        DEBUG("S3WorkerThread.run")
        while True:
            self.__runJob(self.__workQueue.get())
            self.__workQueue.task_done()
            if self.__workQueue.empty():
                self.__wantAbort = False
                self.__S3FS.transferReset()


