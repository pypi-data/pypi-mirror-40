# OutputList.py
#
# Inherits from wx.ListBox and provides some handy methods for printing status
# updates e.g. progress bars for S3 jobs.
#
import wx

from S3WorkerThread import S3EVT_ACTION

class OutputList(wx.ListBox):
    
    def __init__(self, *args, **kwargs):
        super(OutputList, self).__init__(*args, **kwargs) 
            
        self.InitUI()

        
    def InitUI(self):
        self.SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        S3EVT_ACTION(self, self.OnAction) # Actions from S3WorkerThread


    def OnAction(self, e):
        if e.actionID == 1: # Start
            self.startTransfer(e.actionStr)
        elif e.actionID == 2: # Progress
            self.updateTransferProgressPercent(e.actionStr)
        elif e.actionID == 3: # End
            self.endTransfer(e.actionStr)
        elif e.actionID == 4: # Action
            self.doneAction(e.actionStr)
        else:
            DEBUG('Invalid actionID')


    def Append(self, msg):
        rows = msg.split('\n')
        for row in rows:
            index = wx.ListBox.Append(self, row)
        self.SetFirstItem(index)
        return index


    def UpdateRow(self, index, msg):
        self.SetString(index, msg)
        self.SetFirstItem(index)


    def updateTransferProgressPercent(self, pc):
        percentDone = "{0:.0f}%".format(pc)
        if percentDone == '100%':
            numberOfBars = 20
            numberOfSpaces = 0
            printArrow = 0
        else:
            numberOfBars = int(pc * 20 / 100)
            numberOfSpaces = 20 - numberOfBars + (3 - len(percentDone))
            printArrow = 1

#        DEBUG('numberOfBars=' + str(numberOfBars))
#        DEBUG('numberOfSpaces=' + str(numberOfSpaces))

        actionProgressStr = self._action + ' [';
        for i in range(0, numberOfBars):
            actionProgressStr += '='
        if printArrow:
            actionProgressStr += '>'
        for i in range(0, numberOfSpaces):
            actionProgressStr += ' '

        actionProgressStr += percentDone + ']'
#        DEBUG(actionProgressStr)
        self.UpdateRow(self._busyRowNumber, actionProgressStr)


    def startTransfer(self, action):
        if len(action) > 50:
            action = action[:50] + '...'
        self._action = action
        self._busyRowNumber = self.Append(action)
        self.updateTransferProgressPercent(0)


    def endTransfer(self, msg):
        self.UpdateRow(self._busyRowNumber, msg)


    def doneAction(self, msg):
        self.Append(msg)


    def OnRightDown(self, e):
        self.outputListMenu = wx.Menu()
        mi = wx.MenuItem(self.outputListMenu, wx.NewId(), 'Select All')
        self.outputListMenu.AppendItem(mi)
        self.Bind(wx.EVT_MENU, self.OnOutputListSelectAll, mi)
        mi = wx.MenuItem(self.outputListMenu, wx.NewId(), 'Copy')
        self.outputListMenu.AppendItem(mi)
        self.Bind(wx.EVT_MENU, self.OnOutputListCopy, mi)

        self.PopupMenu(self.outputListMenu, e.GetPosition())


    def OnOutputListSelectAll(self, e):
        for i in range(self.GetCount()):
            self.SetSelection(i)


    def OnOutputListCopy(self, e):
        text = ''
        selections = self.GetSelections()
        for i in selections:
            text = text + self.GetString(i) + '\n'

        if wx.TheClipboard.Open():
            wx.TheClipboard.Clear()
            wx.TheClipboard.SetData(wx.TextDataObject(text))
            wx.TheClipboard.Close()


