from PyQt5.QtWidgets import QMainWindow, QApplication,  QListView, QDateTimeEdit, QSlider, QPushButton, QListWidget, QPlainTextEdit
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5 import QtCore
from customTimer import customTimer
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
        
        #define Widgets
        self.dialogBox = self.findChild(QPlainTextEdit,"dialogBox")
        self.listApps = self.findChild(QListView,"listApps")
        self.durationSetter = self.findChild(QSlider,"durationSetter")
        self.lockActivate = self.findChild(QPushButton,"lockActivate")
        self.listStatus = self.findChild(QListWidget,"listStatus")
        self.dateTime = self.findChild(QDateTimeEdit,"dateTime")
        self.dateTime.setDateTime(QtCore.QDateTime.currentDateTime())
        
        #initial dialog messages
        self.dialogBox.appendPlainText("Welcome to FocusHelper. Hope you enjoy it! :)")
        customTimer()
        customTimer(3000,self.dialogBox,"Detecting applications...","Done!")

        
    def setIcon(self):
        appIcon = QIcon("resources/focusIcon.png")
        self.setWindowIcon(appIcon)


        
# Initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_() 