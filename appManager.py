#global arrays
timedApps = []
lockedApps = []
dictOfShortcutTarget = {}
appInOperation = [] 

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
        appInOperation.append(appName)
        
    def removeTimedAppFromList(self,appName):
        timedApps.remove(appName)
        appInOperation.remove(appName)
    
    def getTimedAppName(self,order):
        return timedApps[order]
    
    def exportTimedAppList(self):
        return timedApps
                
    def exportDictOfShortcutTarget(self):
        return dictOfShortcutTarget
    
    def getNumberOfOccupiedApps(self):
        return len(appInOperation)
    
    def exportLockedAppList(self):
        return lockedApps
    
    def getLockedAppName(self,order):
        return lockedApps[order]
    
    def addLockedAppList(self,appName):
        lockedApps.append(appName) 
        appInOperation.append(appName)
    
    def removeLockedAppFromList(self,appName):
        lockedApps.remove(appName)
        appInOperation.remove(appName)
    
    def exportOccupiedAppList(self):
        return appInOperation