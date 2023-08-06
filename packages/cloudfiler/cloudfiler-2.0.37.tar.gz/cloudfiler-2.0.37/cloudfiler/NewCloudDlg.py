# NewCloudDlg
#
# Inherits from wx.Dialog and prompts the user for the connection settings for
# a new S3 cloud service.  This dialog is used by the CloudConnectDlg if the
# user clicks on New.
#
import wx
import AppConfig

class NewCloudDlg(wx.Dialog):

    def __init__(self, *args, **kwargs):
        super(NewCloudDlg, self).__init__(*args, **kwargs) 
        self.InitUI()
        

    def InitUI(self):
        self.SetSize((400, 180))

        label1 = wx.StaticText(self, label='Cloud Service:', pos=(10, 15))
        self.cloudService = wx.TextCtrl(self, pos=(130, 10))
        cw = self.cloudService.GetCharWidth()
        w,h = self.cloudService.GetSize()
        self.cloudService.SetSize((cw * 22, h))

        label2 = wx.StaticText(self, label='Cloud Host:', pos=(10, 45))
        self.cloudHost = wx.TextCtrl(self, pos=(130, 40))
        cw = self.cloudHost.GetCharWidth()
        w,h = self.cloudHost.GetSize()
        self.cloudHost.SetSize((cw * 32, h))

        label3 = wx.StaticText(self, label='Short Name:', pos=(10, 75))
        self.shortName = wx.TextCtrl(self, pos=(130, 70))
        cw = self.shortName.GetCharWidth()
        w,h = self.shortName.GetSize()
        self.shortName.SetSize((cw * 4, h))

        okButton = wx.Button(self, id=wx.ID_OK, label='Ok', pos=(200, 105))
        okButton.Bind(wx.EVT_BUTTON, self.OnClose)
        cancelButton = wx.Button(self, id=wx.ID_CANCEL, label='Cancel', pos=(300, 105))


    def OnClose(self, e):        
        # Validate fields
        cloudName = self.cloudService.GetValue()
        cloudHost = self.cloudHost.GetValue()
        shortName = self.shortName.GetValue().upper()
        if '/' in cloudName or '\\' in cloudName or ':' in cloudName:
            dlg = wx.MessageDialog(None, 'Invalid cloud name (no slashes or colons)', 'Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
        elif len(cloudName) < 1:
            dlg = wx.MessageDialog(None, 'Empty cloud name', 'Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
        elif '/' in cloudHost or '\\' in cloudHost or ':' in cloudHost or ' ' in cloudHost:
            dlg = wx.MessageDialog(None, 'Invalid cloud host (no slashes, spaces or colons)', 'Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
        elif len(cloudHost) < 1:
            dlg = wx.MessageDialog(None, 'Empty cloud host', 'Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
        elif len(shortName) != 2 or not shortName.isalpha():
            dlg = wx.MessageDialog(None, 'Invalid short name (expect two alphabetic characters)', 'Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
        elif AppConfig.HasSection(cloudName):
            dlg = wx.MessageDialog(None, 'Already have a cloud called ' + cloudName, 'Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
        elif self.alreadyGotShortName(shortName):
            dlg = wx.MessageDialog(None, 'Already have a short name = ' + shortName, 'Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
        else:
            self.EndModal(wx.ID_OK)
            

    def alreadyGotShortName(self, shortName):
        for section in AppConfig.GetSections():
            if section != 'History':
                if AppConfig.Get(section, 'ShortName') == shortName:
                    return True
        
        return False


    def GetCloudService(self):
        return self.cloudService.GetValue()


    def GetCloudHost(self):
        return self.cloudHost.GetValue()


    def GetShortName(self):
        return self.shortName.GetValue().upper()


