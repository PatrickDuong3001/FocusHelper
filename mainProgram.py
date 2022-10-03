from PyQt5.QtWidgets import QMainWindow, QApplication, QDateTimeEdit, QSlider, QPushButton, QListWidget, QPlainTextEdit, QMessageBox,QCheckBox,QMenu,QLineEdit,QLabel
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from functools import partial
from PyQt5 import QtCore
from appLocker import appLocker
from appViewer import appViewer
from customTimer import customTimer
from appStopper import appStopper
from appManager import appManager
import sys
from PyQt5.QtCore import QThreadPool, QObject
import emailManager
import time

#Initiate UI
class UI(QMainWindow,QObject):
    ##############################################################Set up UI and prepare applications########################################################################
    def __init__(self):
        super(UI,self).__init__()
        self.ui = loadUi("resources/FocusUI.ui",self)
        self.setFixedSize(915, 616)
        self.setIcon()
        self.setWindowTitle("FocusHelper v1.0")
        self.show() 
        self.pool = QThreadPool()
        self.pool.setMaxThreadCount(12)
        self.emailManage = emailManager.emailManager(self.emailList)
        self.emailManage.setupFile()
                        
        #define Widgets
        self.dialogBox = self.findChild(QPlainTextEdit,"dialogBox")
        self.listApps = self.findChild(QListWidget,"listApps")
        self.listApps2 = self.findChild(QListWidget,"listApps2")
        self.durationSetter = self.findChild(QSlider,"durationSetter")
        self.activate1 = self.findChild(QPushButton,"activate1")
        self.activate2 = self.findChild(QPushButton,"activate2")
        self.dateTime = self.findChild(QDateTimeEdit,"dateTime")
        self.dateTime.setDateTime(QtCore.QDateTime.currentDateTime())
        
        self.emailEnable = self.findChild(QCheckBox,"emailEnable")
        self.emailList = self.findChild(QListWidget,"emailList")
        self.emailInsert = self.findChild(QLineEdit,"emailInsert")
        self.passInsert = self.findChild(QLineEdit,"passInsert")
        self.emailAdd = self.findChild(QPushButton,"emailAdd")
        self.shutDown = self.findChild(QPushButton,"shutDown")
        
        self.emailLabel = self.findChild(QLabel,"emailLabel")
        self.passLabel = self.findChild(QLabel,"passLabel")
        self.addLabel = self.findChild(QLabel,"addLabel")
        self.shutDownLabel = self.findChild(QLabel,"shutDownLabel")
        self.emailListLabel = self.findChild(QLabel,"emailListLabel")
                
        #controls
        self.activate1.setEnabled(False)
        self.activate2.setEnabled(False)
        self.timeStopChosen = False
        self.anAppChosenToStop = False
        self.durationAlreadySet = False
        self.anAppChosenToLock = False
        self.quitAttempt = 0
        self.advancedModeHide()
        
        #menu bar
        option = self.menuBar().addMenu('Options')
        self.advancedMode = option.addAction('Advanced Mode')
        self.normalMode = option.addAction('Normal Mode')
        self.about = option.addAction("About")
        self.instruction = option.addAction("How to Use")
        
        #events
        self.activate2.clicked.connect(self.activatedCountDown)
        self.dateTime.dateTimeChanged.connect(partial(self.setControl,1))
        self.listApps2.itemClicked.connect(partial(self.setControl,2))
        self.listApps.itemClicked.connect(partial(self.setControl,4))
        self.durationSetter.valueChanged.connect(partial(self.setControl,3))
        self.activate1.clicked.connect(self.activateLocker)
        self.advancedMode.triggered.connect(self.advancedModeUnhide) 
        self.normalMode.triggered.connect(self.advancedModeHide)
        self.emailAdd.clicked.connect(self.emailPassHandler)
        self.emailList.installEventFilter(self)
        
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
    #######################################################################################################################################################################
    
    ################################################################These methods handle Emailer and File Writing##########################################################
    def emailPassHandler(self):
        email =  self.emailInsert.text()
        password = self.passInsert.text()
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle("WARNING")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setWindowIcon(QIcon("resources/focusIcon.png"))
        if(len(email) == 0 and len(password) == 0):
            msgBox.setText("Please enter your email and password!")
            msgBox.exec()
        elif(len(email) == 0 and len(password) > 0):
            msgBox.setText("Please enter your email!")
            msgBox.exec()
        elif(len(email) > 0 and len(password) == 0):
            msgBox.setText("Please enter your password!")
            msgBox.exec()
        else: 
            valid = self.emailManage.emailValidator(email)
            print(valid)
            if (valid == 0):
                msgBox.setText("Please enter a valid email!")
                msgBox.exec()
            elif (valid == 1):
                msgBox.setText("Please enter a non-disposable email!")
                msgBox.exec()
            else: 
                self.emailManage.saveEmails(email,password)
                self.emailManage.displayEmailList()
    
    def eventFilter(self, source, event):   #context menu for emails in email list
        if(event.type() == QtCore.QEvent.ContextMenu and source is self.emailList):
            menu = QMenu()
            activateAction = None
            deleteAction = None
            changePassAction = None
            deactivateAction = None
            
            try:
                chosenEmail = source.itemAt(event.pos()).text()
                if self.emailManage.getChosenEmail() == None or len(self.emailManage.getChosenEmail()) == 0:
                    activateAction = menu.addAction("Activate") #the activate option only pops up when there are no currently activated email
                if chosenEmail != self.emailManage.getChosenEmail():
                    deleteAction = menu.addAction("Delete")
                    changePassAction = menu.addAction("Change Password")
                else: 
                    deactivateAction = menu.addAction("Deactivate")
                action = menu.exec_(event.globalPos())
                if action != None:
                    if (action == activateAction):
                        print("Activate")
                        self.passwordPrompt(chosenEmail,0)
                    elif action == deleteAction:
                        print("Delete")
                        self.passwordPrompt(chosenEmail,1)
                    elif action == deactivateAction:
                        self.passwordPrompt(chosenEmail,2)
                        print("deactivate")
                    elif action == changePassAction:
                        print("changePassAction")
                        self.passwordPrompt(chosenEmail,3)
            except:
                print("exception happens")
        return super(UI,self).eventFilter(source, event)
    
    def passwordPrompt(self,email,actionType):
        dlg =  QtWidgets.QInputDialog(self)          
        dlg.setInputMode(QtWidgets.QInputDialog.TextInput) 
        dlg.setLabelText("Please Enter Password:")   
        dlg.setFixedSize(350,100)              
        dlg.setWindowTitle("PASSWORD")       
        dlg.setWindowIcon(QIcon("resources/focusIcon.png"))
        dlg.exec_()   
        #self.emailManage.passwordVerifier(email,dlg.textValue())
        passwordReturn = self.emailManage.passwordVerifier(email,dlg.textValue())
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle("WARNING")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setWindowIcon(QIcon("resources/focusIcon.png"))
        if actionType == 0:
            if passwordReturn == 0:
                msgBox.setText("Wrong/No Password")
                msgBox.exec()
            else:
                self.emailManage.emailActivate(email)
                msgBox.setText("Email Activated")
                msgBox.exec()
        elif actionType == 1: 
            if passwordReturn == 0:
                msgBox.setText("Wrong/No Password")
                msgBox.exec()
            else:
                self.emailManage.deleteEmailFromDict(email)
                self.emailManage.rewriteEmailPasswordListAfterDelete()
                msgBox.setText("Email Deleted")
                msgBox.exec()
        elif actionType == 2:
            if passwordReturn == 0:
                msgBox.setText("Wrong/No Password")
                msgBox.exec()
            else:
                self.emailManage.deleteChosenEmail()
                msgBox.setText("Email Deactivated")
                msgBox.exec()
        elif actionType == 3:
            if passwordReturn == 0:
                msgBox.setText("Wrong/No Password")
                msgBox.exec()
            else:
                time.sleep(0.5)
                dlg.setLabelText("Enter New Password") 
                dlg.exec_()   
                self.emailManage.changeEmailPassword(email,dlg.textValue())
            
    def closeEvent(self, event):
        appManage = appManager().getNumberOfOccupiedApps()
        print(appManage)
        if self.emailManage.getChosenEmail() not in [0,None,""]: 
            if (appManage != 0):
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Critical)
                msgBox.setWindowTitle("ALERT")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.setWindowIcon(QIcon("resources/focusIcon.png"))
                if (self.quitAttempt < 3):
                    self.quitAttempt += 1
                    msgBox.setText(f"Cannot close. Applications under lock or timer!\n Quit attempts: {self.quitAttempt}")
                    msgBox.exec()
                    event.ignore()
                else: 
                    msgBox.setText("Quit attempts exceed 3. Notifying Super User...")
                    msgBox.exec()
                    event.accept()
            else:
                event.accept()
        else: 
            event.accept()
            
    def advancedModeUnhide(self):
        print("unhide??")
        self.emailInsert.show()
        self.passInsert.show()
        self.emailList.show()
        self.shutDown.show()
        self.emailAdd.show()
        self.passLabel.show()
        self.emailLabel.show()
        self.addLabel.show()
        self.shutDownLabel.show()
        self.emailListLabel.show()
        
    def advancedModeHide(self):
        self.emailInsert.hide()
        self.passInsert.hide()
        self.emailList.hide()
        self.shutDown.hide()
        self.emailAdd.hide()
        self.passLabel.hide()
        self.emailLabel.hide()
        self.addLabel.hide()
        self.shutDownLabel.hide()
        self.emailListLabel.hide()
    ###########################################################################################################################################################################      
    
    ################################################################These methods handle Timer and Locker######################################################################
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
                
                self.dateTime.setDateTime(QtCore.QDateTime.currentDateTime())
                self.timeStopChosen = False
                self.anAppChosenToStop = False
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
    ############################################################################################################################################################################
        
# Initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_() 