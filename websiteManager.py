from PyQt5.QtWidgets import QListWidgetItem
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import os
import re
import time

blockedWebList = []
class websiteManager():
    def __init__(self,webList):   
        super().__init__()
        self.webList = webList
                    
    def addToBlockedList(self,web):
        webUrl = None
        if "www." not in web:
            webUrl = "www." + web
            if webUrl not in blockedWebList:
                blockedWebList.append(webUrl)
        else:
            webUrl = web
            if webUrl not in blockedWebList:
                blockedWebList.append(webUrl)
        self.displayWebList()
            
    def displayWebList(self):
        self.webList.clear()
        for web in blockedWebList:
            item = QListWidgetItem()
            item.setText(web)
            self.webList.addItem(item)
    
    def removeWebFromBlockedList(self,web):
        blockedWebList.remove(web)
        self.displayWebList()