from msilib.schema import ListView
from PyQt5 import QtGui
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import glob, os

class appDetector():
    '''
    this class is used to detect on the desktop apps of a Windows device
    '''
    def __init__(self,listView):   
        super().__init__()
        self.desktopPath = os.path.expanduser("~/Desktop")
        self.listView = listView
        
    def appDetect(self):
        for file in os.listdir(self.desktopPath):
            if file.endswith(".url"):
                self.addToListView(file.replace(".url",""))
            elif file.endswith(".lnk"):
                self.addToListView(file.replace(".lnk",""))
    
    def addToListView(self,itemToAdd,timedAppList=None):
        item = QListWidgetItem()
        item.setText(itemToAdd)
        if timedAppList != None and itemToAdd in timedAppList:
            item.setFlags(Qt.NoItemFlags)
        self.listView.addItem(item)
    
    def updateListAppView(self,timedAppList):
        self.listView.clear() 
        for file in os.listdir(self.desktopPath):
            if file.endswith(".url"):
                self.addToListView(file.replace(".url",""),timedAppList)
            elif file.endswith(".lnk"):
                self.addToListView(file.replace(".lnk",""),timedAppList)        
        

if __name__ == "__main__":
    appDetect = appDetector()
    appDetect.appDetect()
    