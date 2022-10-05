from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt
import os
import win32com.client 
from appManager import appManager

class appViewer():
    def __init__(self,listView):   
        super().__init__()
        self.desktopPath = os.path.expanduser("~\Desktop")
        self.listView = listView
        self.apper = appManager()
        self.occupiedApps = self.apper.exportOccupiedAppList()
        
    def appDetect(self):
        shell = win32com.client.Dispatch("WScript.Shell")
        for file in os.listdir(self.desktopPath):
            if file.endswith(".lnk"):
                self.apper.addToDictShortcutTarget(file.replace('.lnk',''),shell.CreateShortCut(os.path.abspath(os.path.join(self.desktopPath,file))).Targetpath)
                self.addToListView(file.replace('.lnk',''))
    
    def addToListView(self,itemToAdd,timedAppList=None):
        item = QListWidgetItem()
        item.setText(itemToAdd)
        if timedAppList != None and itemToAdd in timedAppList:
            item.setFlags(Qt.NoItemFlags)
        self.listView.addItem(item)
    
    def updateListAppView(self):
        self.listView.clear() 
        for file in os.listdir(self.desktopPath):
            if file.endswith(".lnk"):
                self.addToListView(file.replace(".lnk",""),self.occupiedApps)   
                 
    def addTimedAppList(self,appName):
        self.apper.addTimedAppList(appName)
    
    def addLockedAppList(self,appName):
        self.apper.addLockedAppList(appName)
    