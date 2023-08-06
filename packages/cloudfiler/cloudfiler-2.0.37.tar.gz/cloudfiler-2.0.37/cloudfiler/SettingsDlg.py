# SettingsDlg.py
#
# Inherits from wx.Dialog and prompts the user for proxy server settings.
#
import wx

class SettingsDlg(wx.Dialog):

    def __init__(self, *args, **kwargs):
        super(SettingsDlg, self).__init__(*args, **kwargs) 
        
        self.InitUI()

        
    def InitUI(self):
        try:
            currentProxyServer = AppConfig.Get('History', 'ProxyServer')
            currentProxyUsername = AppConfig.Get('History', 'ProxyUsername')
            currentProxyPassword = AppConfig.Get('History', 'ProxyPassword')
        except:
            currentProxyServer = ''
            currentProxyUsername = ''
            currentProxyPassword = ''

        self.SetSize((400, 180))

        label1 = wx.StaticText(self, label='Proxy Server:', pos=(10, 15))
        self.proxyServer = wx.TextCtrl(self, pos=(130, 11))
        self.proxyServer.SetFocus()
        self.proxyServer.SetValue(currentProxyServer)
        cw = self.proxyServer.GetCharWidth()
        w,h = self.proxyServer.GetSize()
        self.proxyServer.SetSize((cw * 32, h))

        label2 = wx.StaticText(self, label='Proxy Username:', pos=(10, 45))
        self.proxyUsername = wx.TextCtrl(self, pos=(130, 41))
        self.proxyUsername.SetValue(currentProxyUsername)
        cw = self.proxyUsername.GetCharWidth()
        w,h = self.proxyUsername.GetSize()
        self.proxyUsername.SetSize((cw * 32, h))

        label3 = wx.StaticText(self, label='Proxy Password:', pos=(10, 75))
        self.proxyPassword = wx.TextCtrl(self, pos=(130, 71))
        self.proxyPassword.SetValue(currentProxyPassword)
        cw = self.proxyPassword.GetCharWidth()
        w,h = self.proxyPassword.GetSize()
        self.proxyPassword.SetSize((cw * 32, h))

        okButton = wx.Button(self, id=wx.ID_OK, label='Ok', pos=(200, 115))
        okButton.Bind(wx.EVT_BUTTON, self.OnClose)
        cancelButton = wx.Button(self, id=wx.ID_CANCEL, label='Cancel', pos=(300, 115))


    def GetProxyServer(self):
        return self.proxyServer.GetValue()


    def GetProxyUsername(self):
        return self.proxyUsername.GetValue()


    def GetProxyPassword(self):
        return self.proxyPassword.GetValue()


    def OnClose(self, e):        
        # Validate fields
        proxyServer = self.proxyServer.GetValue()
        if len(proxyServer) > 0:
            parts = proxyServer.split(":")
            if len(parts) != 2:
                dlg = wx.MessageDialog(None, 'Invalid proxy setting: format should be server:port', 'Error', wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
            else:
                self.EndModal(wx.ID_OK)
        else:
            self.EndModal(wx.ID_OK)


