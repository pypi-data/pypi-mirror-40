#!/usr/bin/python

'''
AppConfig.py

CloudFiler Application configuration module which handles various user
settings.  Settings are either stored in the CloudFiler.ini in the user's home
dir or, for secure settings, in the user's keyring.

'''

import os
from os.path import expanduser
import ConfigParser
import keyring
import shutil

configFullPath = 'uninitialised'
config = ConfigParser.ConfigParser()

def Init(configFilename, factorySettingsDir):
    global configFullPath
    configFullPath = expanduser("~") + os.path.sep + configFilename
    # If the config file does not exist in the user's home folder
    if not os.path.isfile(configFullPath):
        # Copy the factory settings
        factoryFullPath = factorySettingsDir + os.path.sep + configFilename
        shutil.copyfile(factoryFullPath, configFullPath)

    config.read(configFullPath)
    if len(config.sections()) == 0:
        raise Exception('No configuration data found so initialisation failed some how.')

def Get(sectionName, settingName):
    return config.get(sectionName, settingName)

def Set(sectionName, settingName, value):
    config.set(sectionName, settingName, value)

def GetSections():
    return config.sections()

def HasSection(sectionName):
    return config.has_section(sectionName)

def AddSection(sectionName):
    config.add_section(sectionName)

def DelSection(sectionName):
    config.remove_section(sectionName)

def WriteSettings():
    global configFullPath
#    print 'configFullPath='+configFullPath
    fp = open(configFullPath, 'w')
    config.write(fp)
    fp.close()

def SecureGet(sectionName, settingName):
    try:
        value = keyring.get_password(sectionName, settingName)
        if value == None:
            value = ''
    except:
        value = ''
    return value

def SecureSet(sectionName, settingName, value):
    keyring.set_password(sectionName, settingName, value)

