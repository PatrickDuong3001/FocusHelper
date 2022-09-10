from asyncio import threads
import time
from appManager import appManager
from PyQt5.QtCore import pyqtSignal,QRunnable
import subprocess
from appViewer import appViewer
import time
import random

class appStopper(QRunnable):
    '''
    this class checks when to stop an app
    the class adopts multithreading model
    '''
    def __init__(self,targetHour,targetMin,listView):   
        super().__init__()
        self.targetHour = targetHour
        self.targetMin = targetMin 
        self.apps = appManager()
        self.appTarget = self.apps.exportDictOfShortcutTarget()
        self.timedAppList = self.apps.exportTimedAppList()
        self.finished = pyqtSignal()
        self.listView = listView
        
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
        subprocess.call(f"TASKKILL /F /T /IM {appTarget}", shell=True)
        self.apps.removeTimedAppFromList(appName)   
        appViewer(self.listView).updateListAppView()     
    
    def retrieveExeFromAppTarget(self,appFullTarget):
        return appFullTarget.split("\\")[-1]
        
        
            