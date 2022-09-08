from asyncio import threads
import threading
import time
import os, signal
from appManager import appManager

class appStopper():
    '''
    this class checks when to stop an app
    the class adopts multithreading model
    '''
    def __init__(self,targetHour,targetMin):   
        super().__init__()
        self.targetHour = targetHour
        self.targetMin = targetMin 
        self.apps = appManager()
        print("hellohello")
        self.appTarget = self.apps.exportDictOfShortcutTarget()
        self.timedAppList = self.apps.exportTimedAppList()
        
    def timerActivate(self):
        print("hello timer")
        appName = self.apps.getTimedAppName(-1)
        print("after appName")
        appTarget = self.appTarget[appName]
        
        currentHour = time.strftime("%H", time.localtime())       
        print(currentHour)
        currentMin = time.strftime("%M", time.localtime())
        
        print("hello before loop")
        while not(currentHour == self.targetHour and currentMin == self.targetMin):
            currentHour = time.strftime("%H", time.localtime())       
            currentMin = time.strftime("%M", time.localtime())
        self.processKiller(appTarget)
    
    def processKiller(self,appName,appTarget):
        for line in os.popen("ps ax | grep " + appTarget + " | grep -v grep"):
            fields = line.split()
             
            # extracting Process ID from the output
            pid = fields[0]
             
            # terminating process
            os.kill(int(pid), signal.SIGKILL)
        self.apps.removeTimedAppFromList(appName)
        print("Process Successfully terminated")
        
            
    def initiateMultithreadTimer(self):
        l = len(self.timedAppList)
        t = threading.Thread(target=timeCompare, args=(l,))
        threads.append(t)
        t.start()
        
        
        
        
if __name__ == "__main__":
    timeCompare = appStopper()
    timeCompare.timeCompare()
        
            