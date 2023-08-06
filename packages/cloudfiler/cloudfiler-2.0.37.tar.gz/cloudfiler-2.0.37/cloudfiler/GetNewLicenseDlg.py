# GetNewLicenseDlg
#
# Inherits from wx.Dialog and prompts the user for a new licence key.
#
import wx
import Utils

class GetNewLicenseDlg(wx.Dialog):

    def __init__(self, licMsg, *args, **kwargs):
        super(GetNewLicenseDlg, self).__init__(*args, **kwargs) 
        
        self.InitUI(licMsg)

        
    def InitUI(self, licMsg):
        self.SetSize((400, 130))

        label0 = wx.StaticText(self, label=licMsg, pos=(10, 15))

        label1 = wx.StaticText(self, label='License Key:', pos=(10, 45))
        self.licenseKey = wx.TextCtrl(self, pos=(106, 41))
        self.licenseKey.SetFocus()
        cw = self.licenseKey.GetCharWidth()
        w,h = self.licenseKey.GetSizeTuple()
        self.licenseKey.SetSize((cw * 32, h))

        okButton = wx.Button(self, id=wx.ID_OK, label='Ok', pos=(200, 75))
        okButton.Bind(wx.EVT_BUTTON, self.OnClose)
        cancelButton = wx.Button(self, id=wx.ID_CANCEL, label='Cancel', pos=(300, 75))


    def OnClose(self, e):        
        # Validate fields
        licenseKey = self.licenseKey.GetValue()
        if len(licenseKey) < 1:
            dlg = wx.MessageDialog(None, 'Empty key', 'Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
        else:
            self.EndModal(wx.ID_OK)


    def GetKey(self):
        return Utils.ensure_ascii(self.licenseKey.GetValue().strip())


