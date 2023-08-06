# NewFolderDlg
#
# Inherits from wx.Dialog and prompts the user for a valid folder name.
#
import wx

class NewFolderDlg(wx.Dialog):

    def __init__(self, *args, **kwargs):
        super(NewFolderDlg, self).__init__(*args, **kwargs) 
        
        self.InitUI()

        
    def InitUI(self):
        self.SetSize((400, 130))

        label1 = wx.StaticText(self, label='Folder name:', pos=(10, 15))
        self.newName = wx.TextCtrl(self, pos=(106, 11))
        self.newName.SetFocus()
        cw = self.newName.GetCharWidth()
        w,h = self.newName.GetSize()
        self.newName.SetSize((cw * 32, h))

        okButton = wx.Button(self, id=wx.ID_OK, label='Ok', pos=(200, 65))
        okButton.Bind(wx.EVT_BUTTON, self.OnClose)
        cancelButton = wx.Button(self, id=wx.ID_CANCEL, label='Cancel', pos=(300, 65))


    def OnClose(self, e):        
        # Validate fields
        newName = self.newName.GetValue()
        if newName.startswith('_CF'):
            dlg = wx.MessageDialog(None, 'Invalid name (cannot start with _CF)', 'Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
        elif len(newName) < 1:
            dlg = wx.MessageDialog(None, 'Empty name', 'Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
        else:
            self.EndModal(wx.ID_OK)


    def GetName(self):
        return self.newName.GetValue()


