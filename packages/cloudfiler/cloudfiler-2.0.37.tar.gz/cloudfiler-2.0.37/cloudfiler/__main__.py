#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# CloudFiler.py
#
# Main GUI script.  For a description of what CloudFiler does see:
#
# https://cloud-filer.sourceforge.io/
#
# The icons used in Cloud Filer are open source and from the following sources:
#
# Page-world, Film, Lock, Package, Image, Word, Excel & Powerpoint from
#    http://findicons.com/pack/1588/farm_fresh_web by FatCow Web Hosting
#    (http://creativecommons.org/licenses/by/3.0/)
#
# Others from http://openiconlibrary.sourceforge.net/
#    (Either public domain or http://creativecommons.org/licenses/by-sa/1.0/)
#

import sys
import wx

def IsWX4():
    return wx.VERSION[0] >= 4

if IsWX4():
    import wx.adv
    
import os
import encodings.hex_codec
import encodings.ascii
import encodings.utf_8
import encodings.idna
import Utils
import AppConfig

from Queue import Queue
from FileListCtrl import FileListCtrl
from Utils import DEBUG

TEST_LICENSING = len(sys.argv) > 1 and sys.argv[1] == '--test-licensing'
if TEST_LICENSING:
    import Licensing
else:
    import NullLicensing as Licensing

from OutputList import OutputList
from GetNewLicenseDlg import GetNewLicenseDlg
from CloudConnectDlg import CloudConnectDlg
from SettingsDlg import SettingsDlg
from S3WorkerThread import S3WorkerThread

ID_LOCAL_DIR_COMBO = wx.NewId()
ID_REMOTE_DIR_COMBO = wx.NewId()
ID_REMOTE_CONNECT = wx.NewId()
ID_OPEN_HELP = wx.NewId()
ID_OPEN_HELP_ABOUT = wx.NewId()
ID_LOCAL_UPLOAD = wx.NewId()
ID_REMOTE_DOWNLOAD = wx.NewId()
ID_OPEN_HELP_LICENSING = wx.NewId()
ID_FILE_SETTINGS = wx.NewId()
ID_REMOTE_CANCEL = wx.NewId()

CF_VERSION_STRING = '2.0'

class MainForm(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(MainForm, self).__init__(*args, **kwargs) 
            
        self.accessKey = None
        self.secretKey = None
        self.password = None
        
        Utils.set_main_dir() # Find out where we are installed so we can pick up stuff like icon images

        AppConfig.Init('CloudFiler.ini', Utils.get_main_dir()) # Initial ini file is in script dir

        # Initialise proxy settings
        try:
            self.proxyServer = AppConfig.Get('History', 'ProxyServer')
            self.proxyUsername = AppConfig.Get('History', 'ProxyUsername')
            self.proxyPassword = AppConfig.Get('History', 'ProxyPassword')
        except:
            self.proxyServer = ''
            self.proxyUsername = ''
            self.proxyPassword = ''

        if self.CheckLicensed(self.proxyServer, self.proxyUsername, self.proxyPassword):
            self.InitUI()

        
    def InitUI(self):

        self._queue = Queue()

        self.icon = wx.Icon(Utils.GetFilePath(Utils.ICON_APPLICATION), wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        
#        icon = wx.IconFromBitmap(wx.Bitmap(GetIconPath(Utils.ICON_REMOTE_FOLDER)))
#        self.SetIcon(icon)#, TRAY_TOOLTIP)

#        image = wx.Image(GetIconPath(Utils.ICON_APPLICATION), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
#        icon = wx.EmptyIcon()
#        icon.CopyFromBitmap(image)
#        self.SetIcon(icon)

#        ib = wx.IconBundle()
#        ib.AddIconFromFile(GetIconPath(Utils.ICON_REMOTE_FOLDER), wx.BITMAP_TYPE_PNG)
#        self.SetIcons(ib)
        
        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        fileMenu.Append(wx.ID_OPEN, '&Open')
        fileMenu.Append(ID_REMOTE_CONNECT, '&Connect')
        fileMenu.Append(ID_FILE_SETTINGS, '&Settings')
        fileMenu.AppendSeparator()

        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+W')
        fileMenu.AppendItem(qmi)

        self.Bind(wx.EVT_MENU, self.OnQuit, qmi)

        transferMenu = wx.Menu()
        transferMenu.Append(ID_LOCAL_UPLOAD, 'Upload')
        transferMenu.Append(ID_REMOTE_DOWNLOAD, 'Download')
        transferMenu.Append(ID_REMOTE_CANCEL, 'Cancel')

        helpMenu = wx.Menu()
        helpMenu.Append(ID_OPEN_HELP, 'User Guide')
        helpMenu.Append(ID_OPEN_HELP_LICENSING, 'Licensing')
        helpMenu.Append(ID_OPEN_HELP_ABOUT, 'About')

        menubar.Append(fileMenu, '&File')
        menubar.Append(transferMenu, '&Transfer')
        menubar.Append(helpMenu, '&Help')
        self.SetMenuBar(menubar)

        toolbar = self.CreateToolBar()
        toolbar.SetBackgroundColour('#E0E0E0')
        qtool = toolbar.AddLabelTool(wx.ID_OPEN, 'Open', wx.Bitmap(Utils.GetFilePath(Utils.ICON_FOLDER)), shortHelp='Open')
        qtool = toolbar.AddLabelTool(ID_REMOTE_CONNECT, 'Connect', wx.Bitmap(Utils.GetFilePath(Utils.ICON_REMOTE_FOLDER)), shortHelp='Connect')
        toolbar.AddSeparator()
        qtool = toolbar.AddLabelTool(ID_OPEN_HELP, 'Help', wx.Bitmap(Utils.GetFilePath(Utils.ICON_HELP_CONTENTS)), shortHelp='Help')
        qtool = toolbar.AddLabelTool(ID_OPEN_HELP_ABOUT, 'About', wx.Bitmap(Utils.GetFilePath(Utils.ICON_HELP_ABOUT)), shortHelp='About')
        toolbar.Realize()

        # Create the outer horizontal splitter with a vertical splitter above
        # and the output text box below

        self.hsplitter = wx.SplitterWindow(self, -1)
        self.hsplitter.SetMinimumPaneSize(10)

        # Create the top half of the horizontal splitter
        self.vsplitter = wx.SplitterWindow(self.hsplitter, -1)
        self.vsplitter.SetMinimumPaneSize(10)

        # Create the top left
        topLeftPanel = wx.Panel(self.vsplitter, -1)
        topLeftPanel.SetBackgroundColour('#E0E0E0')
        topRightPanel = wx.Panel(self.vsplitter, -1)
        topRightPanel.SetBackgroundColour('#E0E0E0')

        self.localDirCombo = wx.ComboBox(topLeftPanel, ID_LOCAL_DIR_COMBO, style=wx.TE_PROCESS_ENTER)
#        self.localDirCombo.SetStringSelection(homeDirPath)

        self.localFileList = FileListCtrl(topLeftPanel, -1, style=wx.LC_REPORT)

        topLeftSizer = wx.BoxSizer(wx.VERTICAL)
        topLeftSizer.Add(self.localDirCombo, 0, wx.EXPAND, 1)
        topLeftSizer.Add(self.localFileList, 1, wx.EXPAND | wx.ALL, 1)
        topLeftPanel.SetSizer(topLeftSizer)


        # Create the top right
        self.remoteIcon = wx.StaticBitmap(topRightPanel, bitmap=wx.Bitmap(Utils.GetFilePath(Utils.ICON_RED_SHIELD)), size=(16,16))
        self.remoteDirCombo = wx.ComboBox(topRightPanel, ID_REMOTE_DIR_COMBO, style=wx.TE_PROCESS_ENTER|wx.TE_READONLY)

        topRightIconComboSizer = wx.BoxSizer(wx.HORIZONTAL)
        topRightIconComboSizer.Add(self.remoteIcon, 0, wx.EXPAND|wx.LEFT|wx.TOP, border=4)
        topRightIconComboSizer.Add(self.remoteDirCombo, 1, wx.EXPAND|wx.LEFT, border=4)

        self.remoteFileList = FileListCtrl(topRightPanel, -1, style=wx.LC_REPORT)
#        self.remoteFileList.SetBackgroundColour(wx.Colour(200,240,200))

        topRightSizer = wx.BoxSizer(wx.VERTICAL)
        topRightSizer.Add(topRightIconComboSizer, 0, wx.EXPAND, 1)
        topRightSizer.Add(self.remoteFileList, 1, wx.EXPAND | wx.ALL, 1)
        topRightPanel.SetSizer(topRightSizer)

        self.vsplitter.SplitVertically(topLeftPanel, topRightPanel)
        

        # Create the bottom half of the horizontal splitter
        bottomPanel = wx.Panel(self.hsplitter, -1)
        bottomPanel.SetBackgroundColour('#E0E0E0')

        self.outputList = OutputList(bottomPanel, style=wx.LB_EXTENDED)

        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer.Add(self.outputList, 1, wx.EXPAND | wx.ALL, 1)

        bottomPanel.SetSizer(bottomSizer)

        self.hsplitter.SplitHorizontally(self.vsplitter, bottomPanel)

        # Setup events
        self.Bind(wx.EVT_TEXT_ENTER, self.OnLocalDirText, id=ID_LOCAL_DIR_COMBO)
        self.Bind(wx.EVT_COMBOBOX, self.OnLocalDirText, id=ID_LOCAL_DIR_COMBO)
        self.Bind(wx.EVT_MENU, self.OnBrowseLocal, id=wx.ID_OPEN)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnRemoteDirText, id=ID_REMOTE_DIR_COMBO)
        self.Bind(wx.EVT_COMBOBOX, self.OnRemoteDirText, id=ID_REMOTE_DIR_COMBO)
        self.Bind(wx.EVT_MENU, self.OnBrowseRemote, id=ID_REMOTE_CONNECT)
        self.Bind(wx.EVT_MENU, self.OnFileSettings, id=ID_FILE_SETTINGS)
        self.Bind(wx.EVT_MENU, self.OnOpenHelp, id=ID_OPEN_HELP)
        self.Bind(wx.EVT_MENU, self.OnOpenHelpAbout, id=ID_OPEN_HELP_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnOpenHelpLicensing, id=ID_OPEN_HELP_LICENSING)

        self.Bind(wx.EVT_MENU, self.OnLocalUpload, id=ID_LOCAL_UPLOAD)
        self.Bind(wx.EVT_MENU, self.OnRemoteDownload, id=ID_REMOTE_DOWNLOAD)
        self.Bind(wx.EVT_MENU, self.OnCancelTransfer, id=ID_REMOTE_CANCEL)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        # Open initial local directory
        homeDirPath = os.path.expanduser("~")
        localDirList = [homeDirPath]
        self.localFileList.Init(self._queue, None, self.localDirCombo, self.outputList, self.remoteFileList)
        self.localFileList.SetDir(homeDirPath)
        self.localDirCombo.Append(homeDirPath)
        self.localDirCombo.SetStringSelection(homeDirPath)

        # Initialise the remote directory list control
        self.remoteFileList.Init(self._queue, self.remoteIcon, self.remoteDirCombo, self.outputList, None)

        self._worker = S3WorkerThread(self._queue, self.localFileList, self.remoteFileList, self.outputList)
        self._worker.setDaemon(True)
        self._worker.start()

        self.SetSize((1200, 800))
        self.SetTitle('Cloud Filer')
        self.Centre()
#        self.Show(True)
        

#    def OnIdle(self, e):
#        global gbl_newerVersionAvailable
#        if gbl_newerVersionAvailable:
#            gbl_newerVersionAvailable = False
#            self.Unbind(wx.EVT_IDLE, handler=self.OnIdle)
#            msg = 'Download a new version from:\n\n'
#            msg = msg + '    http://www.nuvovis.com'
#            dlg = Utils.InformationDlg('New version available!', msg, False, True, self, wx.ID_ANY, 'Cloud Filer - Information')
#            dlg.ShowModal()
#            if dlg.GetEnoughAlready():
#                AppConfig.Set('History', 'UserSupressedVersionCheck', 'Y')
#                AppConfig.WriteSettings()
#            dlg.Destroy()


    def OnSize(self, e):
        width, height = e.GetSize().Get()
        self.vsplitter.SetSashPosition(width / 2, True)
        self.hsplitter.SetSashPosition(height / 2, True)
        e.Skip()


    def OnLocalUpload(self, e):
        self.localFileList.OnUpload(None)


    def OnRemoteDownload(self, e):
        self.remoteFileList.OnDownload(None)


    def OnCancelTransfer(self, e):
        self._worker.abort()


    def OnOpenHelp(self, e):
        DEBUG('OnOpenHelp: os.name=' + os.name)
        try:
            docPath = Utils.GetFilePath(Utils.USER_GUIDE_APPLICATION)
            DEBUG('docPath=' + docPath)
            if Utils.GetOS() == Utils.ID_OS_WINDOWS:
                os.startfile(docPath) # Windows
            elif Utils.GetOS() == Utils.ID_OS_LINUX:
                os.system("xdg-open "+docPath) # Linux
            elif Utils.GetOS() == Utils.ID_OS_MACOS:
                os.system('open', docPath) # MacOS
            else:
                DEBUG('Unexpected OS')
        except Exception as ex:
            DEBUG(str(ex))
            DEBUG('Open help exception (is a PDF reader installed?)')


    def OnOpenHelpLicensing(self, e):
        msg = 'Licensed to ' + Licensing.GetClientName() + '\n'
#       msg = msg + 'License key: ' + Licensing.GetLicenseKey() + '\n'
        if (Licensing.IsPerpetual()):
            msg = msg + 'License never expires\n'
        else:
            msg = msg + 'License expires on ' + Licensing.GetExpiryDate() + '\n'
        if (Licensing.EncryptionModuleLicensed()):
            msg = msg + 'Encryption Module Licensed\n'
        else:
            msg = msg + 'Encryption Module not Licensed\n'
        dlg = Utils.InformationDlg(Licensing.GetAppName(), msg, False, False, self, wx.ID_ANY, 'Cloud Filer - License Details')
        dlg.ShowModal()
        dlg.Destroy()


    def OnOpenHelpAbout(self, e):
        
        description = """
Cloud Filer is an S3 file storage GUI client.  Cloud Filer
allows you to upload and download files to cloud storage
(e.g. Amazon or Google) and can be used as part of a backup
strategy.  Cloud Filer uses TNO, pre-internet encryption and
file name obfuscation making access to your cloud data
useless without the right password.

For information about updates check out the website.
"""

        licence = """
The MIT License (MIT)

Copyright (c) 2019 Nuvovis

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the
Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall
be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
        if IsWX4():
            info = wx.adv.AboutDialogInfo()
        else:
            info = wx.AboutDialogInfo()
 
        info.SetName('Cloud Filer')
        info.SetVersion(CF_VERSION_STRING)
        info.SetDescription(description)
        info.SetCopyright('(C) 2019 Nuvovis')
        info.SetWebSite('https://www.cloudfiler.org/')
        info.SetLicence(licence)

        if IsWX4():
            wx.adv.AboutBox(info)
        else:
            wx.AboutBox(info)

    def OnLocalDirText(self, e):
        newDir = self.localDirCombo.GetValue()
        if os.path.isdir(newDir):
            self.localFileList.SetDir(newDir)
        else:
            self.outputList.Append('Invalid dir: ' + newDir)


    def OnRemoteDirText(self, e):
        newDir = self.remoteDirCombo.GetValue()
        self.remoteFileList.ChangeRemoteDir(newDir)


    def OnBrowseLocal(self, e):
        dlg = wx.DirDialog(self, 'Select a local folder', style=wx.DD_CHANGE_DIR|wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.localDirCombo.Append(dlg.GetPath())
            self.localDirCombo.SetStringSelection(dlg.GetPath())
            self.localFileList.SetDir(dlg.GetPath())

        dlg.Destroy()


    def CheckLicensed(self, proxyServer, proxyUsername, proxyPassword):
        '''Checks CloudFiler is licensed.  In the open source version on
        Sourceforge the licensing check does nothing and just succeeds - it uses
        the NullLicensing.py implementation.
        '''
        if Licensing.CloudFilerLicensed():
            return True

        # Initialise licensing
        try:
            key = AppConfig.Get('History', 'LicenseKey')
            DEBUG('LicenseKey=' + key)
        except:
            key = ''
        Licensing.Init(os.path.realpath(Utils.get_main_dir()), key, proxyServer, proxyUsername, proxyPassword)
        if not Licensing.CloudFilerLicensed():
            dlg = GetNewLicenseDlg(Licensing.GetLicensingMsg(), self, wx.ID_ANY, 'License Cloud Filer')
            if dlg.ShowModal() == wx.ID_OK:
                DEBUG('Activating license...')
                key = dlg.GetKey()
                Licensing.Init(os.path.realpath(Utils.get_main_dir()), key, proxyServer, proxyUsername, proxyPassword)
                if Licensing.CloudFilerLicensed():
                    DEBUG('License retireved...')
                    AppConfig.Set('History', 'LicenseKey', key)
                    AppConfig.WriteSettings()
                    self.OnOpenHelpLicensing(None)
                else:
                    DEBUG('License no good')
                    errorMsg = 'Failed to activate license: ' + Licensing.GetLicensingMsg()
                    errorMsg += '\nCheck proxy settings?'
                    dlg2 = wx.MessageDialog(None, errorMsg, 'Error', wx.OK | wx.ICON_ERROR)
                    dlg2.ShowModal()

            dlg.Destroy()

        return Licensing.CloudFilerLicensed()

    def OnBrowseRemote(self, e):
        if self.GetCloudCredentials():
            cxn = self.remoteFileList.S3Connect(self.accessKey, self.secretKey, self.password, self.proxyServer, self.proxyUsername, self.proxyPassword, self._cloudService, self._cloudHost, self._cloudRootText)
            if self.remoteFileList.IsConnected():
                self.remoteFileList.ChangeRemoteDir(self._cloudRootText + '/')
                self._worker.setConnection(cxn, self._cloudRootText, self.password)
            else:
                self.outputList.Append('Not connected!')


    def GetCloudCredentials(self):
        dlg = CloudConnectDlg(self, wx.ID_ANY, 'Specify cloud connection')
        if dlg.ShowModal() == wx.ID_OK:
            self.accessKey = dlg.GetAccessKey()
            self.secretKey = dlg.GetSecretKey()
            self.password = dlg.GetPassword()
            self._cloudService = dlg.GetCloudService()
            self._cloudHost = dlg.GetCloudHost()
            self._cloudRootText = dlg.GetRootText()
            keyKey = 'nuvovis.com CloudFiler ' + self._cloudRootText.rstrip(':')
            import unicodedata
            keyKey = unicodedata.normalize('NFKD', keyKey).encode('ascii', 'ignore')
            if dlg.StoreKeys():
                AppConfig.SecureSet(keyKey, 'AK', self.accessKey)
                AppConfig.SecureSet(keyKey, 'SK', self.secretKey)
            else:
                AppConfig.SecureSet(keyKey, 'AK', '')
                AppConfig.SecureSet(keyKey, 'SK', '')
            
            if dlg.StorePassword():
                AppConfig.SecureSet(keyKey, 'PWD', self.password)
            else:
                AppConfig.SecureSet(keyKey, 'PWD', '')

            if not dlg.GetEncrypt():
                self.password = '' # Switch off encryption now that we have saved the password if necessary

            dlg.SaveLastConnection() 
# With later keyring can use delete_password
# keyring.delete_password('AWSS3', 'AK')
# keyring.delete_password('AWSS3', 'SK')

#            self.remoteFileList.SetRemoteDir(self._cloudRootText)
            hitOk = True

        else:
            hitOk = False

        dlg.Destroy()
        return hitOk


    def OnFileSettings(self, e):
        dlg = SettingsDlg(self, wx.ID_ANY, 'Settings')
        if dlg.ShowModal() == wx.ID_OK:
            self.proxyServer = dlg.GetProxyServer()
            self.proxyUsername = dlg.GetProxyUsername()
            self.proxyPassword = dlg.GetProxyPassword()
            AppConfig.Set('History', 'ProxyServer', self.proxyServer)
            AppConfig.Set('History', 'ProxyUsername', self.proxyUsername)
            AppConfig.Set('History', 'ProxyPassword', self.proxyPassword)
            AppConfig.WriteSettings()

        dlg.Destroy()


    def OnQuit(self, e):
        Licensing.UnInit(os.path.realpath(Utils.get_main_dir()))
        self.Close()



def main():
    app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
    locale = wx.Locale(wx.LANGUAGE_ENGLISH)
    frame = MainForm(None)
    frame.Show(True)     # Show the frame.
    app.MainLoop()


if __name__ == '__main__':
    main()

