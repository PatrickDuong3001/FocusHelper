from asyncio import threads
import threading
import time
import os, signal
from appManager import appManager
from PyQt5.QtCore import pyqtSignal,QRunnable
import subprocess
from appViewer import appViewer

class appStopper(QRunnable):
    '''
    this class checks when to stop an app
    the class adopts multithreading model
    '''
    def __init__(self,targetHour,targetMin):   
        super().__init__()
        self.targetHour = targetHour
        self.targetMin = targetMin 
        self.apps = appManager()
        self.appTarget = self.apps.exportDictOfShortcutTarget()
        self.timedAppList = self.apps.exportTimedAppList()
        self.finished = pyqtSignal()
        
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
        subprocess.call(f"TASKKILL /F /T /IM {appTarget}", shell=True)
        self.apps.removeTimedAppFromList(appName)        
    
    def retrieveExeFromAppTarget(self,appFullTarget):
        return appFullTarget.split("\\")[-1]
        
        
            