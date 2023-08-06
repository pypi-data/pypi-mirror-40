#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Licensing.py

Wrapper class for Nuvovis licensing API.

This is not used by the free open source version of Cloud Filer.  It is used in
special builds as an example of a licensed python application. 

'''

import os
import ctypes
import time
import Utils

PWD = '7kyPaVIG7U1yqdd0fA65oKvnIVcAw3et8QLdUtpkVTioJaXWCZG5sGDg'
APP_NAME = 'Cloud Filer'
APP_VER = 'v2.0'
CRYPTO_FEATURE_NAME = 'CRYPTO'
CRYPTO_FEATURE_VALUE = 'okay'

if Utils.GetOS() == Utils.ID_OS_WINDOWS:
    PGSLIC_DLL = 'pgslicmt.dll'
else:
    PGSLIC_DLL = 'libPGSLIC.so'

LICENSE_OK = 0
LICENSE_WARNING = 1
LICENSE_ERROR = 2
LICENSE_EXPIRED = 3
LICENSE_STALE = 4

global m_licenseKey
global m_licensed
global m_encryptionLicensed
global m_licMsg
global m_appName
global m_clientName
global m_expiryDate
global m_isPerpetual

m_licenseKey = ''
m_licensed = False
m_encryptionLicensed = False
m_licMsg = 'Not initialised'
m_appName = ''
m_clientName = ''
m_expiryDate = ''
m_isPerpetual = 0


def CloudFilerLicensed():
    global m_licensed
    return m_licensed

def EncryptionModuleLicensed():
    global m_encryptionLicensed
    return m_encryptionLicensed

def GetLicenseKey():
    global m_licenseKey
    return m_licenseKey

def GetAppName():
    global m_appName
    return m_appName

def GetClientName():
    global m_clientName
    return m_clientName

def GetExpiryDate():
    global m_expiryDate
    return m_expiryDate

def IsPerpetual():
    global m_isPerpetual
    return m_isPerpetual

def GetLicensingMsg():
    global m_licMsg
    return m_licMsg

def Init(installPath, key, proxyServer, proxyUsername, proxyPassword):
    global m_licenseKey
    global m_licensed
    global m_encryptionLicensed
    global m_licMsg
    global m_appName
    global m_clientName
    global m_expiryDate
    global m_isPerpetual

    Utils.DEBUG('Licensing.Init: installPath=' + installPath)
    Utils.DEBUG('Licensing.Init: key=' + key)

    if len(key) > 0:
#        PGSLIC_DLL_PATH = installPath + os.sep + PGSLIC_DLL
        Utils.DEBUG('Loading licensing DLL ' + PGSLIC_DLL)
        licDLL = ctypes.CDLL(PGSLIC_DLL)
        appInfoStr = APP_VER + ' ' + time.strftime("%d %b %Y %H%M", time.gmtime())
        cxnStr = "PXSP=" + proxyServer + "&PXUN=" + proxyUsername + "&PXPW=" + proxyPassword + "&PXAT=ANY"
        status = licDLL.checkLicense('.', PWD, key, APP_NAME, appInfoStr, cxnStr)
        if (status == LICENSE_OK):
            m_licenseKey = key
            m_licensed = True
            m_licMsg = 'Valid license found'
            licDLL.getAppName.restype = ctypes.c_char_p
            m_appName = licDLL.getAppName()
            licDLL.getClientName.restype = ctypes.c_char_p
            m_clientName = licDLL.getClientName().decode('utf-8')
            licDLL.getExpiryDate.restype = ctypes.c_char_p
            m_expiryDate = licDLL.getExpiryDate()
            licDLL.isPerpetual.restype = ctypes.c_int
            m_isPerpetual = licDLL.isPerpetual()
            licDLL.getSetting.restype = ctypes.c_char_p
            cryptoLicCode = licDLL.getSetting(CRYPTO_FEATURE_NAME)
            if cryptoLicCode == CRYPTO_FEATURE_VALUE:
                m_encryptionLicensed = True

        elif (status == LICENSE_ERROR):
            licDLL.getLastError.restype = ctypes.c_char_p
            m_licMsg = 'License error - ' + licDLL.getLastError()
        elif (status == LICENSE_EXPIRED):
            licDLL.getExpiryDate.restype = ctypes.c_char_p
            m_licMsg = 'License expired on ' + licDLL.getExpiryDate()
        else:
            raise Exception('Invalid status from pgslic.checkLicense')
    else:
        m_licMsg = 'License key not found'

def UnInit(installPath):
    Utils.DEBUG('Licensing.UnInit: installPath=' + installPath)
    if (m_licensed):
        PGSLIC_DLL_PATH = installPath + os.sep + PGSLIC_DLL
        licDLL = ctypes.CDLL(PGSLIC_DLL_PATH)
        status = licDLL.release(PWD)

