from PyQt5.QtWidgets import QMainWindow, QApplication, QDateTimeEdit, QSlider, QPushButton, QListWidget, QPlainTextEdit, QListWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from customTimer import customTimer
from appDetector import appDetector
import sys
import os

#Initiate UI
class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        uic.loadUi("resources/FocusUI.ui",self)
        self.setFixedSize(915, 616)
        self.setIcon()
        self.show() 
        
        #controls
        self.timedApps = []
        self.lockedApps = []
        
        #define Widgets
        self.dialogBox = self.findChild(QPlainTextEdit,"dialogBox")
        self.listApps = self.findChild(QListWidget,"listApps")
        self.listApps2 = self.findChild(QListWidget,"listApps2")
        self.durationSetter = self.findChild(QSlider,"durationSetter")
        self.activate1 = self.findChild(QPushButton,"activate1")
        self.activate2 = self.findChild(QPushButton,"activate1")
        self.dateTime = self.findChild(QDateTimeEdit,"dateTime")
        self.dateTime.setDateTime(QtCore.QDateTime.currentDateTime())
        
        #events
        #self.listApps.itemClicked.connect(self.updateList)
        self.activate1.clicked.connect(self.activatedCountDown1)
        
        #initial dialog messages
        self.dialogBox.appendPlainText("Welcome to FocusHelper. Hope you enjoy it! :)")
        customTimer()
        customTimer(3000,self.dialogBox,"Detecting applications...","Done!")
        
        #display list of apps 
        self.appDetect1 = appDetector(self.listApps)
        self.appDetect2 = appDetector(self.listApps2)
        self.appDetect1.appDetect()
        self.appDetect2.appDetect()
        

    def activatedCountDown1(self):
        items = self.listApps.selectedItems()
        for item in items:
            self.timedApps.append(item.text())
        self.appDetect1.updateListAppView(self.timedApps)

    
        
        
    def setIcon(self):
        appIcon = QIcon("resources/focusIcon.png")
        self.setWindowIcon(appIcon)
    
    
            
    
    
    #item.setFlags(Qt.NoItemFlags) #grey out an item



        
# Initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_() 