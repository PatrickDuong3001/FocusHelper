import os
import win32com.client 

#global arrays
timedApps = []
dictOfShortcutTarget = {}

class appManager():
    '''
    this class is used to detect on the desktop apps of a Windows device
    '''
    def __init__(self):   
        super().__init__()
        print("inside appManager??")
                
    def addToDictShortcutTarget(self,appName,appTarget):
        dictOfShortcutTarget[appName] = appTarget
        
    def addTimedAppList(self,appName):
        timedApps.append(appName) 
        
    def removeTimedAppFromList(self,appName):
        timedApps.remove(appName)
    
    def getTimedAppName(self,order):
        return timedApps[order]
    
    def exportTimedAppList(self):
        return timedApps
                
    def exportDictOfShortcutTarget(self):
        return dictOfShortcutTarget
    