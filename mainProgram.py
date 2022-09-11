from PyQt5.QtWidgets import QMainWindow, QApplication, QDateTimeEdit, QSlider, QPushButton, QListWidget, QPlainTextEdit, QMessageBox
from PyQt5.QtGui import QIcon
from functools import partial
from PyQt5 import uic
from PyQt5 import QtCore
from appLocker import appLocker
from appViewer import appViewer
from customTimer import customTimer
from appStopper import appStopper
from appManager import appManager
import sys
from PyQt5.QtCore import QThreadPool, QObject, QRunnable, pyqtSignal
import os

#Initiate UI
class UI(QMainWindow,QObject):
    def __init__(self):
        super(UI,self).__init__()
        uic.loadUi("resources/FocusUI.ui",self)
        self.setFixedSize(915, 616)
        self.setIcon()
        self.show() 
        self.pool = QThreadPool()
        self.pool.setMaxThreadCount(6)
        
        #controls
        #self.timedApps = []
        #self.lockedApps = []
        
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
        self.durationAlreadySet = False
        self.anAppChosenToLock = False
        
        #events
        self.activate2.clicked.connect(self.activatedCountDown)
        self.dateTime.dateTimeChanged.connect(partial(self.setControl,1))
        self.listApps2.itemClicked.connect(partial(self.setControl,2))
        self.listApps.itemClicked.connect(partial(self.setControl,4))
        self.durationSetter.valueChanged.connect(partial(self.setControl,3))
        self.activate1.clicked.connect(self.activateLocker)
        
        #initial dialog messages
        self.dialogBox.appendPlainText("Welcome to FocusHelper. Hope you enjoy it! :)")
        customTimer()
        customTimer(1000,self.dialogBox,"Detecting applications...","Done!")
        self.activate1.setEnabled(True)
        self.activate2.setEnabled(True)
        
        #display list of apps 
        self.appDetect1 = appViewer(self.listApps)
        self.appDetect2 = appViewer(self.listApps2)
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
        elif controlType == 3: #durationAlreadySet signal
            self.durationAlreadySet = True
        elif controlType == 4: #anAppChosenToLock signal
            self.anAppChosenToLock = True 
            
    def activatedCountDown(self):            
        if (self.anAppChosenToStop and self.timeStopChosen) == True:
            if (appManager().getNumberOfOccupiedApps() < 6):
                items = self.listApps2.selectedItems()
                print("in if")
                for item in items:
                    self.appDetect2.addTimedAppList(item.text())
                self.appDetect1.updateListAppView()
                self.appDetect2.updateListAppView()    
                
                #extract time value from QTimeEdit
                targetHour = self.dateTime.time().toString("hh")
                targetMin = self.dateTime.time().toString("mm")
                            
                self.appStop = appStopper(targetHour,targetMin,self.listApps,self.listApps2)
                self.pool.start(self.appStop.timerActivate)
                
                self.timeStopChosen = False
                self.anAppChosenToStop = False
                self.dateTime.setDateTime(QtCore.QDateTime.currentDateTime())
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setWindowTitle("WARNING")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.setText("Cannot set lock or timer on 6+ applications!")
                msgBox.exec()
        else:
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
        
    
    def activateLocker(self):
        if(self.durationAlreadySet and self.anAppChosenToLock) == True:
            if (appManager().getNumberOfOccupiedApps() < 6):
                items = self.listApps.selectedItems()
                print("in if locker??")
                for item in items:
                    self.appDetect1.addLockedAppList(item.text())
                self.appDetect1.updateListAppView()
                self.appDetect2.updateListAppView()
                
                #extract duration from slider
                duration = self.durationSetter.value() * 600    #duration in secconds
                
                self.appLock = appLocker(duration,self.listApps,self.listApps2)
                self.pool.start(self.appLock.countDownLockerActivate)
                
                self.durationAlreadySet = False
                self.anAppChosenToLock = False
            else: 
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setWindowTitle("WARNING")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.setText("Cannot set lock or timer on 6+ applications!")
                msgBox.exec()
        else: 
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("WARNING")
            msgBox.setStandardButtons(QMessageBox.Ok)
            if (self.anAppChosenToLock == False) and (self.durationAlreadySet == False):
                msgBox.setText("Please select a duration and an app")
            elif (self.anAppChosenToLock == True) and (self.durationAlreadySet == False):
                msgBox.setText("Please select a duration")
            else: 
                msgBox.setText("Please select an app")
            msgBox.exec()
    


        
# Initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_() 