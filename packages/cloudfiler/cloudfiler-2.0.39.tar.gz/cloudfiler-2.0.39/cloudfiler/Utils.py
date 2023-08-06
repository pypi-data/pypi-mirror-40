# -*- coding: utf-8 -*-
import os
import wx
import sys

ACTION_DELETE_BUCKET = 1
ACTION_UPLOAD_FILE = 2
ACTION_DELETE_FILE = 3
ACTION_DELETE_FOLDER = 4
ACTION_DOWNLOAD_FILE = 5
ACTION_DELETE_CLOUD = 6
ACTION_BETA_EXPIRED = 8

# First icon IDs correspond with the FileListCtrl.il wx.ImageList
ICON_UP_DIR = 0
ICON_FOLDER = 1
ICON_DOC_PLAIN = 2
ICON_LOCK = 3
ICON_DOC_TEXT = 4
ICON_DOC_PDF = 5
ICON_DOC_IMAGE = 6
ICON_PACKAGE = 7
ICON_MUSIC = 8
ICON_FILM = 9
ICON_SUBTITLES = 10
ICON_CDROM = 11
ICON_SCRIPT_PYTHON = 12
ICON_DOC_WORD = 13
ICON_DOC_EXCEL = 14
ICON_DOC_POWERPOINT = 15
ICON_DOC_HTML = 16
ICON_SIGNATURE = 17
ICON_REMOTE_FOLDER = 18
ICON_CSS = 19
ICON_SCRIPT = 20
ICON_EXE = 21
ICON_LIB = 22
ICON_DLL = 23
ICON_SMALL_ARROW_DOWN = 24
ICON_SMALL_ARROW_UP = 25
ICON_GREEN_SHIELD = 26
ICON_RED_SHIELD = 27

ICON_WARNING = 100
ICON_UPLOAD_MERGE = 101
ICON_HELP_CONTENTS = 102
ICON_HELP_ABOUT = 103
ICON_APPLICATION = 104
USER_GUIDE_APPLICATION = 105
ICON_INFORMATION = 106

ID_SKIP_BUTTON = 104

ID_OS_LINUX = 1
ID_OS_MACOS = 2
ID_OS_WINDOWS = 3


def DEBUG(msg):
# Uncomment the following line for debug output
#    print 'DEBUG:', msg.encode('utf-8', errors='replace')
    pass


def GetOS():
    if os.name == 'posix':
        # Either Linux or MacOS
        DEBUG('sys.platform=' + sys.platform)
        if sys.platform.lower().startswith('linux'):
            return ID_OS_LINUX
        else:
            return ID_OS_MACOS
    else:
        return ID_OS_WINDOWS


def ensure_unicode(x):
    if not isinstance(x, unicode):
        return unicode(x.decode('utf-8'))
    else:
        return x


def ensure_ascii(x):
    if not isinstance(x, str):
        return str(x.encode('ascii'))
    else:
        return x


def filename_from_path(path):
    lastSlashPos = path.rfind('/')
    if lastSlashPos >= 0:
        return path[lastSlashPos+1:]
    else:
        return path


def set_main_dir():
    global gbl_main_dir
    if '__file__' not in globals():
        # Use next 2 lines and sys.executable if building with py2exe on Windows or freeze *nix
        DEBUG('os.path.dirname(sys.executable)=' + os.path.dirname(sys.executable))
        gbl_main_dir = os.path.dirname(sys.executable)
    else:
        # Use next 2 lines and sys.executable if running as an interpreted python script
        DEBUG('os.path.dirname(os.path.realpath(__file__))=' + os.path.dirname(os.path.realpath(__file__)))
        gbl_main_dir = os.path.dirname(os.path.realpath(__file__))

def get_main_dir():
    global gbl_main_dir
    return gbl_main_dir
    

def get_images_dir():
    return get_main_dir() + os.sep + 'images'


def GetFilePath(iconId):
    if iconId == USER_GUIDE_APPLICATION:
        path = os.path.realpath(get_main_dir())
        return path + os.sep + 'CloudFilerUserGuide.pdf'

    path = os.path.realpath(get_images_dir())
    
    if iconId == ICON_WARNING:
        return path + os.sep + 'pictogram-din-w000-general.png'
    elif iconId == ICON_INFORMATION:
        return path + os.sep + 'pictogram-din-m000-general.png'
    elif iconId == ICON_FOLDER:
        return path + os.sep + 'document-open-folder.png'
    elif iconId == ICON_REMOTE_FOLDER:
        return path + os.sep + 'document-open-remote.png'
    elif iconId == ICON_UP_DIR:
        return path + os.sep + 'go-up-5.png'
    elif iconId == ICON_DOC_PLAIN:
        return path + os.sep + 'application-x-zerosize.png'
    elif iconId == ICON_LOCK:
        return path + os.sep + 'lock.png'
    elif iconId == ICON_DOC_TEXT:
        return path + os.sep + 'text_align_left.png'
    elif iconId == ICON_DOC_PDF:
        return path + os.sep + 'application-pdf.png'
    elif iconId == ICON_DOC_IMAGE:
        return path + os.sep + 'image.png'
    elif iconId == ICON_PACKAGE:
        return path + os.sep + 'package.png'
    elif iconId == ICON_MUSIC:
        return path + os.sep + 'music.png'
    elif iconId == ICON_FILM:
        return path + os.sep + 'film.png'
    elif iconId == ICON_SUBTITLES:
        return path + os.sep + 'text-x-dtd.png'
    elif iconId == ICON_CDROM:
        return path + os.sep + 'cd.png'
    elif iconId == ICON_SCRIPT_PYTHON:
        return path + os.sep + 'text-x-python.png'
    elif iconId == ICON_DOC_WORD:
        return path + os.sep + 'word.png'
    elif iconId == ICON_DOC_EXCEL:
        return path + os.sep + 'excel.png'
    elif iconId == ICON_DOC_POWERPOINT:
        return path + os.sep + 'powerpoint.png'
    elif iconId == ICON_DOC_HTML:
        return path + os.sep + 'page_world.png'
    elif iconId == ICON_SIGNATURE:
        return path + os.sep + 'text_signature.png'
    elif iconId == ICON_UPLOAD_MERGE:
        return path + os.sep + 'go-next-2.png'
    elif iconId == ICON_HELP_CONTENTS:
        return path + os.sep + 'help-contents-5.png'
    elif iconId == ICON_HELP_ABOUT:
        return path + os.sep + 'help.png'
    elif iconId == ICON_CSS:
        return path + os.sep + 'css.png'
    elif iconId == ICON_SCRIPT:
        return path + os.sep + 'script_gear.png'
    elif iconId == ICON_EXE:
        return path + os.sep + 'cog.png'
    elif iconId == ICON_LIB:
        return path + os.sep + 'page_link.png'
    elif iconId == ICON_DLL:
        return path + os.sep + 'link.png'
    elif iconId == ICON_APPLICATION:
        return path + os.sep + 'app.ico'
    elif iconId == ICON_SMALL_ARROW_DOWN:
        return path + os.sep + 'bullet_arrow_down.png'
    elif iconId == ICON_SMALL_ARROW_UP:
        return path + os.sep + 'bullet_arrow_up.png'
    elif iconId == ICON_GREEN_SHIELD:
        return path + os.sep + 'shield_green.png'
    elif iconId == ICON_RED_SHIELD:
        return path + os.sep + 'shield_red.png'

    raise Exception('Unexpecetd icon id: ' + str(iconId))


class WarningDlg(wx.Dialog):

    def __init__(self, action, showApplyToAll, objectName, *args, **kwargs):
        super(WarningDlg, self).__init__(*args, **kwargs) 
        
        self.InitUI(action, showApplyToAll, objectName)

        
    def InitUI(self, action, showApplyToAll, objectName):
        if showApplyToAll:
            self.SetSize((400, 290))
        else:
            self.SetSize((400, 220))

        if len(objectName) > 32:
            objectName = objectName[:32] + '...'

        if action == ACTION_DELETE_BUCKET:
            title = 'Delete bucket?'
            msg = 'You are about to delete the bucket\n\n\t' + objectName + '\n\nand all its files.'
        elif action == ACTION_DELETE_FILE:
            title = 'Delete file?'
            msg = 'You are about to delete\n\n\t' + objectName
        elif action == ACTION_DELETE_FOLDER:
            title = 'Delete folder?'
            msg = 'You are about to delete\n\n\t' + objectName + '\n\nand all its files.'
        elif action == ACTION_DELETE_CLOUD:
            title = 'Delete cloud settings?'
            msg = 'You are about to delete\n\n\t' + objectName + '\n\nand all its settings.'
        else:
            raise Exception('Unexpected action')

        icon = wx.StaticBitmap(self, bitmap=wx.Bitmap(GetFilePath(ICON_WARNING)), pos=(10, 15))

        label1 = wx.StaticText(self, label=title, pos=(70, 15))
        DEBUG(msg)
        label1.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        label2 = wx.StaticText(self, label=msg, pos=(70, 45), size=(380,100))

        if showApplyToAll:
            self.repeatCheckbox = wx.CheckBox(self, label='Apply this action to all', pos=(70, 165))

            okButton = wx.Button(self, id=wx.ID_OK, label='Ok', pos=(100, 220))
            skipButton = wx.Button(self, id=ID_SKIP_BUTTON, label='Skip', pos=(200, 220))
            cancelButton = wx.Button(self, id=wx.ID_CANCEL, label='Cancel', pos=(300, 220))
        else:
            okButton = wx.Button(self, id=wx.ID_OK, label='Ok', pos=(100, 150))
            skipButton = wx.Button(self, id=ID_SKIP_BUTTON, label='Skip', pos=(200, 150))
            cancelButton = wx.Button(self, id=wx.ID_CANCEL, label='Cancel', pos=(300, 150))

        cancelButton.SetFocus()

        okButton.Bind(wx.EVT_BUTTON, self.OnClose)
        skipButton.Bind(wx.EVT_BUTTON, self.OnClose)
        cancelButton.Bind(wx.EVT_BUTTON, self.OnClose)
        
        
    def OnClose(self, e):        
        self.endId = e.GetId()
        self.Destroy()


    def GetEndId(self):
        return self.endId


    def GetApplyAll(self):
        return self.repeatCheckbox.GetValue()



class InformationDlg(wx.Dialog):

    def __init__(self, title, msg, warning, enoughAlready, *args, **kwargs):
        super(InformationDlg, self).__init__(*args, **kwargs) 
        
        self.InitUI(title, msg, warning, enoughAlready)

        
    def InitUI(self, title, msg, warning, enoughAlready):
        self.SetSize((400, 220))

        if warning:
            icon = wx.StaticBitmap(self, bitmap=wx.Bitmap(GetFilePath(ICON_WARNING)), pos=(10, 15))
        else:
            icon = wx.StaticBitmap(self, bitmap=wx.Bitmap(GetFilePath(ICON_INFORMATION)), pos=(10, 15))

        label1 = wx.StaticText(self, label=title, pos=(70, 15))
        DEBUG(msg)
        label1.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        label2 = wx.StaticText(self, label=msg, pos=(70, 45), size=(300, 75))

        if enoughAlready:
            self.enoughAlreadyCheckbox = wx.CheckBox(self, label='No need to show this again', pos=(70, 120))

        okButton = wx.Button(self, id=wx.ID_OK, label='Ok', pos=(300, 150))

        okButton.Bind(wx.EVT_BUTTON, self.OnClose)
        okButton.SetFocus()
        
        
    def OnClose(self, e):        
        self.EndModal(0)


    def GetEnoughAlready(self):
        return self.enoughAlreadyCheckbox.GetValue()


