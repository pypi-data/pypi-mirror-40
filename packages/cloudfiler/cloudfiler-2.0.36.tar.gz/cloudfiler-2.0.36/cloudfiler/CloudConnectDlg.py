# CloudConnectDlg
#
# Inherits from wx.Dialog and prompts the user for the connection settings when
# connecting to an S3 cloud service.
#
import wx
import AppConfig
import Utils
from Utils import DEBUG
from NewCloudDlg import NewCloudDlg
import sys

TEST_LICENSING = len(sys.argv) > 1 and sys.argv[1] == '--test-licensing'
if TEST_LICENSING:
    import Licensing
else:
    import NullLicensing as Licensing


ID_CLOUD_COMBO = wx.NewId()
ID_DELETE_CLOUD = wx.NewId()
ID_CLOUD_ENCRYPT = wx.NewId()
ID_NEW_CLOUD = wx.NewId()

class CloudConnectDlg(wx.Dialog):

    def __init__(self, *args, **kwargs):
        super(CloudConnectDlg, self).__init__(*args, **kwargs) 
            
        self.InitUI()
        

    def InitUI(self):
        self.SetSize((430, 415)) # Y size = OkButton YPos + 70

        # Cloud connection fields
        label1 = wx.StaticText(self, label='Cloud Service:', pos=(10, 15))
        self.cloudCombo = wx.ComboBox(self, ID_CLOUD_COMBO, style=wx.TE_PROCESS_ENTER, pos=(130, 10)) 
        delButton = wx.Button(self, id=ID_DELETE_CLOUD, label='Delete', pos=(330, 10))
        for section in AppConfig.GetSections():
            if section != 'History':
                self.cloudCombo.Append(section)
        self.cloudCombo.Append('New...')

        label2 = wx.StaticText(self, label='Cloud Host:', pos=(10, 45))
        label3 = wx.StaticText(self, label='Short Name:', pos=(10, 75))

        self.hostText = wx.StaticText(self, pos=(130, 45))
        self.rootText = wx.StaticText(self, pos=(130, 75))

        # Cloud authentication fields
        box1 = wx.StaticBox(self, label='User', pos=(5, 100), size=(410, 115))

        label4 = wx.StaticText(self, label='Access Key:', pos=(10, 125))
        label5 = wx.StaticText(self, label='Secret Key:', pos=(10, 155))

        self.accessKey = wx.TextCtrl(self, style=wx.TE_PASSWORD, pos=(130, 121))
        cw = self.accessKey.GetCharWidth()
        w,h = self.accessKey.GetSize()
        self.accessKey.SetSize((cw * 35, h))

        self.secretKey = wx.TextCtrl(self, style=wx.TE_PASSWORD, pos=(130, 151))
        cw = self.secretKey.GetCharWidth()
        w,h = self.secretKey.GetSize()
        self.secretKey.SetSize((cw * 35, h))

        self.storeKeys = wx.CheckBox(self, label='Save keys', pos=(130, 181))

        # Encryption fields
        box2 = wx.StaticBox(self, label='Security', pos=(5, 220), size=(410, 105))
        self.encrypt = wx.CheckBox(self, id=ID_CLOUD_ENCRYPT, label='Encrypt', pos=(130, 235))

        self.passwordLabel = wx.StaticText(self, label='Password:', pos=(10, 265))
        self.passwordLabel.Enable(False)

        self.password = wx.TextCtrl(self, style=wx.TE_PASSWORD, pos=(130, 261))
        self.password.Enable(False)
        cw = self.password.GetCharWidth()
        w,h = self.password.GetSize()
        self.password.SetSize((cw * 35, h))

        self.storePassword = wx.CheckBox(self, label='Save password', pos=(130, 291))
        self.storePassword.Enable(False)

        if not Licensing.EncryptionModuleLicensed():
            self.encrypt.Enable(False)

        # Bottom buttons
        okButton = wx.Button(self, id=wx.ID_OK, label='Ok', pos=(230, 345))
        cancelButton = wx.Button(self, id=wx.ID_CANCEL, label='Cancel', pos=(330, 345))

        # Wire up events
        self.Bind(wx.EVT_COMBOBOX, self.OnChangeCloud, id=ID_CLOUD_COMBO)
        self.Bind(wx.EVT_BUTTON, self.OnNewCloud, id=ID_NEW_CLOUD)
        self.Bind(wx.EVT_BUTTON, self.OnDeleteCloud, id=ID_DELETE_CLOUD)
        self.Bind(wx.EVT_CHECKBOX, self.OnChangeEncrypt, id=ID_CLOUD_ENCRYPT)
        okButton.Bind(wx.EVT_BUTTON, self.OnClose)

        # Set the combobox selection
        selectedCloud = AppConfig.Get('History', 'LastCloud')
        try:
            sn = AppConfig.Get(selectedCloud, 'ShortName')
            if len(sn) == 0:
                raise Exception('That doesnt look any good to me')
        except:
            selectedCloud = AppConfig.GetSections()[0] # Didn't find that cloud so use the first
        self.SetCloudSelection(selectedCloud)

        okButton.SetFocus()


    def OnClose(self, e):        
        # Validate fields
        if self.encrypt.GetValue() and len(self.password.GetValue()) < 4:
            dlg = wx.MessageDialog(None, 'Invalid password (must be at least 4 characters long)', 'Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
        elif len(self.accessKey.GetValue()) < 1:
            dlg = wx.MessageDialog(None, 'Invalid access key (must be at least 1 character long)', 'Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
        elif len(self.secretKey.GetValue()) < 1:
            dlg = wx.MessageDialog(None, 'Invalid secret key (must be at least 1 character long)', 'Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
        else:
            self.EndModal(wx.ID_OK)


    def OnChangeEncrypt(self, e):
        if self.encrypt.GetValue() and Licensing.EncryptionModuleLicensed():
            self.password.Enable(True)
            self.passwordLabel.Enable(True)
            self.storePassword.Enable(True)
            try:
                suppressWarn = AppConfig.Get('History', 'UserSupressedPasswordWarning')
            except:
                suppressWarn = 'N'
            if suppressWarn != 'Y':
                msg = 'Note that you must remember your password!\n'
                msg = msg + 'Without your password there is no way to\n'
                msg = msg + 'recover your data.'
                dlg = Utils.InformationDlg('Cloud Data Encryption', msg, True, True, self, wx.ID_ANY, 'Cloud Filer - Warning')
                dlg.ShowModal()
                if dlg.GetEnoughAlready():
                    AppConfig.Set('History', 'UserSupressedPasswordWarning', 'Y')
                    AppConfig.WriteSettings()
                dlg.Destroy()

        else:
            self.password.Enable(False)
            self.passwordLabel.Enable(False)
            self.storePassword.Enable(False)


    def SetCloudSelection(self, selection):
        self.cloudCombo.SetStringSelection(selection)

        try:
            cloudHost = AppConfig.Get(selection, 'Host')
        except:
            cloudHost = ''

        try:
            shortName = AppConfig.Get(selection, 'ShortName')
        except:
            shortName = ''

        try:
            saveKeys = AppConfig.Get(selection, 'SaveKeys')
            if saveKeys == 'Y':
                self.storeKeys.SetValue(True)
            else:
                self.storeKeys.SetValue(False)
        except:
            self.storeKeys.SetValue(False)

        try:
            encrypt = AppConfig.Get(selection, 'Encrypt')
            if encrypt == 'Y' and Licensing.EncryptionModuleLicensed():
                self.encrypt.SetValue(True)
            else:
                self.encrypt.SetValue(False)
        except:
            self.encrypt.SetValue(False)
        if self.encrypt.GetValue():
            DEBUG('encrypt=Y')
            self.password.Enable(True)
            self.passwordLabel.Enable(True)
            self.storePassword.Enable(True)
        else:
            DEBUG('encrypt=N')
            self.password.Enable(False)
            self.passwordLabel.Enable(False)
            self.storePassword.Enable(False)

        try:
            storePassword = AppConfig.Get(selection, 'StorePassword')
            if storePassword == 'Y' and Licensing.EncryptionModuleLicensed():
                self.storePassword.SetValue(True)
            else:
                self.storePassword.SetValue(False)
        except:
            self.storePassword.SetValue(False)
        if self.storePassword.GetValue():
            DEBUG('storePassword=Y')
        else:
            DEBUG('storePassword=N')

        self.hostText.ClearBackground()
        self.hostText.SetLabel(cloudHost)
        self.rootText.ClearBackground()
        self.rootText.SetLabel(shortName + ':')

        keyKey = 'nuvovis.com CloudFiler ' + AppConfig.Get(selection, 'ShortName')
        DEBUG('keyKey=' + keyKey)
        pw = AppConfig.SecureGet(keyKey, 'AK')
        DEBUG('AK=' + pw)
        self.accessKey.SetValue(pw)

        pw = AppConfig.SecureGet(keyKey, 'SK')
        DEBUG('SK=' + pw)
        self.secretKey.SetValue(pw)

        if Licensing.EncryptionModuleLicensed():
            pw = AppConfig.SecureGet(keyKey, 'PWD')
        else:
            pw = ''
        DEBUG('PWD=' + pw)
        self.password.SetValue(pw)


    def SaveLastConnection(self):
        newSection = 'History'
        if not AppConfig.HasSection(newSection):
            AppConfig.AddSection(newSection)
        cloudService = self.cloudCombo.GetStringSelection()
        DEBUG('cloudService=' + cloudService)
        if self.storeKeys.IsChecked():
            saveKeys = 'Y'
        else:
            saveKeys = 'N'
        DEBUG('saveKeys=' + saveKeys)
        if self.encrypt.IsChecked():
            encrypt = 'Y'
        else:
            encrypt = 'N'
        DEBUG('encrypt=' + encrypt)
        if self.storePassword.IsChecked():
            storePassword = 'Y'
        else:
            storePassword = 'N'
        DEBUG('storePassword=' + storePassword)

        AppConfig.Set(newSection, 'LastCloud', cloudService)
        AppConfig.Set(cloudService, 'SaveKeys', saveKeys)
        AppConfig.Set(cloudService, 'Encrypt', encrypt)
        AppConfig.Set(cloudService, 'StorePassword', storePassword)
        AppConfig.WriteSettings()


    def PopupNewCloudDlg(self):
        dlg = NewCloudDlg(self, wx.ID_ANY, 'Add new cloud')
        if dlg.ShowModal() == wx.ID_OK:
            newSection = dlg.GetCloudService()
            AppConfig.AddSection(newSection)
            AppConfig.Set(newSection, 'Host', dlg.GetCloudHost())
            AppConfig.Set(newSection, 'ShortName', dlg.GetShortName())
            AppConfig.WriteSettings()
            self.cloudCombo.Insert(newSection, self.cloudCombo.GetCount()-1)
            self.SetCloudSelection(newSection)
        else:
            DEBUG('TODO: select the first one')

        dlg.Destroy()


    def OnDeleteCloud(self, e):
        oldCloud = self.cloudCombo.GetValue()
        if oldCloud != 'New...':
            action = Utils.ACTION_DELETE_CLOUD
            dlg = Utils.WarningDlg(action, False, oldCloud, self, wx.ID_ANY, 'Cloud Filer - Warning')
            dlg.ShowModal()
            status = dlg.GetEndId()
            dlg.Destroy()
            if status == wx.ID_OK:
                AppConfig.DelSection(oldCloud)
                AppConfig.WriteSettings()
                self.cloudCombo.Delete(self.cloudCombo.FindString(oldCloud))
                for section in AppConfig.GetSections():
                    if section != 'History':
                        self.SetCloudSelection(section)


    def OnNewCloud(self, e):
        self.PopupNewCloudDlg()


    def OnChangeCloud(self, e):
        newCloud = self.cloudCombo.GetValue()
        if newCloud == 'New...':
            self.PopupNewCloudDlg()
        else:
            self.SetCloudSelection(newCloud)


    def GetAccessKey(self):
        return self.accessKey.GetValue()


    def GetSecretKey(self):
        return self.secretKey.GetValue()


    def GetEncrypt(self):
        return self.encrypt.IsChecked()


    def GetPassword(self):
        return self.password.GetValue()


    def StoreKeys(self):
        return self.storeKeys.GetValue()


    def StorePassword(self):
        return self.storePassword.GetValue()


    def GetCloudService(self):
        return self.cloudCombo.GetValue()


    def GetCloudHost(self):
        return self.hostText.GetLabelText()


    def GetRootText(self):
        return self.rootText.GetLabelText()


