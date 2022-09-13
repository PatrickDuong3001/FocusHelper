from appManager import appManager
from PyQt5.QtCore import QRunnable
import subprocess
from appViewer import appViewer
import time
import random

class appStopper(QRunnable):
    '''
    this class checks when to stop an app
    the class adopts multithreading model
    '''
    def __init__(self,targetHour,targetMin,listView1,listView2):   
        super().__init__()
        self.targetHour = targetHour
        self.targetMin = targetMin 
        self.apps = appManager()
        self.appTarget = self.apps.exportDictOfShortcutTarget()
        self.timedAppList = self.apps.exportTimedAppList()
        self.listView1 = listView1
        self.listView2 = listView2
        
    def timerActivate(self):
        appName = self.apps.getTimedAppName(-1)
        appTarget = self.appTarget[appName]
        appTarget = self.retrieveExeFromAppTarget(appTarget)

        currentHour = time.strftime("%H", time.localtime())       
        currentMin = time.strftime("%M", time.localtime())
        print("compare??")
        while not(currentHour == self.targetHour and currentMin == self.targetMin):
            currentHour = time.strftime("%H", time.localtime())       
            currentMin = time.strftime("%M", time.localtime())
        self.processKiller(appName,appTarget)
        print("reach the end??")
    
    def processKiller(self,appName,appTarget):
        print("inside process killer??")
        time.sleep(random.randint(1,15))
        subprocess.call(f"TASKKILL /F /T /IM {appTarget} >nul 2>&1", shell=True)
        self.apps.removeTimedAppFromList(appName)   
        appViewer(self.listView1).updateListAppView()
        appViewer(self.listView2).updateListAppView()     
    
    def retrieveExeFromAppTarget(self,appFullTarget):
        return appFullTarget.split("\\")[-1]
        
        
            