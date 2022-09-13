from appManager import appManager
from PyQt5.QtCore import QRunnable
import subprocess
from appViewer import appViewer
import time
import random

class appLocker(QRunnable):
    '''
    this class put a lock on an app
    the class adopts multithreading model
    '''
    def __init__(self,duration,listView1,listView2):   
        super().__init__()
        self.apps = appManager()
        self.appTarget = self.apps.exportDictOfShortcutTarget()
        self.lockedAppList = 0
        self.duration = duration 
        self.listView1 = listView1
        self.listView2 = listView2
    
    def countDownLockerActivate(self):
        appName = self.apps.getLockedAppName(-1)
        appTarget = self.appTarget[appName]
        appTarget = self.retrieveExeFromAppTarget(appTarget)
        
        while (self.duration > 0):
            self.duration -= 1
            time.sleep(1)
            self.processChecker(appTarget)
        time.sleep(random.randint(1,15))
        self.apps.removeLockedAppFromList(appName) 
        appViewer(self.listView1).updateListAppView()
        appViewer(self.listView2).updateListAppView()
            
    def processChecker(self,appTarget):
        try:
            subprocess.call(f"TASKKILL /F /T /IM {appTarget} >nul 2>&1", shell=True)
        except subprocess.CalledProcessError:
            pass
    
    def retrieveExeFromAppTarget(self,appFullTarget):
        return appFullTarget.split("\\")[-1]