from PyQt5.QtWidgets import QMainWindow, QApplication, QDateTimeEdit, QSlider, QPushButton, QListWidget, QPlainTextEdit, QMessageBox
from PyQt5.QtGui import QIcon
from functools import partial
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
        self.activate2 = self.findChild(QPushButton,"activate2")
        self.dateTime = self.findChild(QDateTimeEdit,"dateTime")
        self.dateTime.setDateTime(QtCore.QDateTime.currentDateTime())
        
        #controls
        self.activate1.setEnabled(False)
        self.activate2.setEnabled(False)
        self.timeStopChosen = False
        self.anAppChosenToStop = False
        
        #events
        self.activate2.clicked.connect(self.activatedCountDown)
        self.dateTime.dateTimeChanged.connect(partial(self.setControl,1))
        self.listApps2.itemClicked.connect(partial(self.setControl,2))
        
        #initial dialog messages
        self.dialogBox.appendPlainText("Welcome to FocusHelper. Hope you enjoy it! :)")
        customTimer()
        customTimer(1000,self.dialogBox,"Detecting applications...","Done!")
        self.activate1.setEnabled(True)
        self.activate2.setEnabled(True)
        
        #display list of apps 
        self.appDetect1 = appDetector(self.listApps)
        self.appDetect2 = appDetector(self.listApps2)
        self.appDetect1.appDetect()
        self.appDetect2.appDetect()
        
    def setIcon(self):
        appIcon = QIcon("resources/focusIcon.png")
        self.setWindowIcon(appIcon)
        
    def setControl(self,controlType):
        if controlType == 1: #timeStopChosen signal
            self.timeStopChosen = True 
        elif controlType == 2: #anAppChosenToStop signal
            self.anAppChosenToStop = True
    
    def activatedCountDown(self):
        if (self.anAppChosenToStop and self.timeStopChosen) == True:
            items = self.listApps2.selectedItems()
            for item in items:
                self.timedApps.append(item.text())
            self.appDetect2.updateListAppView(self.timedApps)    
            self.timeStopChosen = False
            self.anAppChosenToStop = False
        else:
            self.showDialog()
    
    def showDialog(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle("WARNING")
        msgBox.setStandardButtons(QMessageBox.Ok)
        if (self.anAppChosenToStop == False) and (self.timeStopChosen == False):
            msgBox.setText("Please select a time and an app")
        elif (self.anAppChosenToStop == True) and (self.timeStopChosen == False):
            msgBox.setText("Please select a time")
        else: 
            msgBox.setText("Please select an app")
        msgBox.exec()
    
    


        
# Initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_() 