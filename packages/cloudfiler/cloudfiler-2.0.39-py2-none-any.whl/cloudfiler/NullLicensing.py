#!/usr/bin/python

'''
NullLicensing.py

Dummy licensing class to switch off licensing.

'''

APP_NAME = 'Cloud Filer'

def CloudFilerLicensed():
    return True 

def EncryptionModuleLicensed():
    return True 

def GetLicenseKey():
    return 'Null key'

def GetAppName():
    return APP_NAME

def GetClientName():
    return 'Everyone'

def GetExpiryDate():
    return '4000-12-31'

def IsPerpetual():
    return True

def GetLicensingMsg():
    return 'Null license'

def Init(installPath, key):
    pass

def UnInit(installPath):
    pass

