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
import subprocess
import emailSender
import websiteManager
import ctypes
import os
from PyQt5.QtGui import QDesktopServices
import os
import wget
import time

#Initiate UI
class UI(QMainWindow,QObject):
    ##############################################################Set up UI and prepare applications########################################################################
    def __init__(self):
        super(UI,self).__init__()
        self.ui = loadUi(os.path.join(FocusHelperPath,"FocusUI.ui"),self)
        self.setFixedSize(915, 750)
        self.setIcon()
        self.setWindowTitle("FocusHelper v1.0")
        self.show() 
        self.pool = QThreadPool()
        self.pool.setMaxThreadCount(12)
        self.emailManage = emailManager.emailManager(self.emailList)
        self.emailManage.setupFile()
        self.errorFormat = '<span style="color:red">{}</span>'
        self.warningFormat = '<span style="color:yellow">{}</span>'
        self.validFormat = '<span style="color:green">{}</span>'
        self.webManage = websiteManager.websiteManager(self.webList)
                        
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
        
        self.webAdder = self.findChild(QPushButton,"webAdder")
        self.webInsert = self.findChild(QLineEdit,"webInsert")
        self.webList = self.findChild(QListWidget,"webList")
                
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
        info = self.menuBar().addMenu('Info')
        self.advancedMode = option.addAction('Advanced Mode')
        self.normalMode = option.addAction('Normal Mode')
        self.about = info.addAction("About")
        self.instruction = info.addAction("How to Use")
        
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
        self.shutDown.clicked.connect(self.forcedShutDown)
        self.emailList.installEventFilter(self)
        self.webAdder.clicked.connect(self.addToBlockList)
        self.webList.installEventFilter(self)
        self.about.triggered.connect(self.displayAbout)
        
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
        appIcon = QIcon(os.path.join(FocusHelperPath,"focusIcon.png"))
        self.setWindowIcon(appIcon)
    #######################################################################################################################################################################
    
    #########################################################These methods handle Website Blocker and HTML display#########################################################
    def addToBlockList(self):
        web = self.webInsert.text()
        if web != None and len(web) != 0:
            self.webManage.addToBlockedList(web)
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("WARNING")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.setWindowIcon(QIcon(os.path.join(FocusHelperPath,"focusIcon.png")))
            msgBox.setText("Restart Browser to see effect")
            msgBox.exec()
    
    def displayAbout(self):
        self.view = QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(os.path.join(FocusHelperPath,"Home.html")))
    #context menu for the blocked web list is handled by the eventFilter() method in the Emailer and File Writing section below
    #######################################################################################################################################################################
    
    ################################################################These methods handle Emailer and File Writing##########################################################
    def emailPassHandler(self):
        email =  self.emailInsert.text()
        password = self.passInsert.text()
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle("WARNING")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setWindowIcon(QIcon(os.path.join(FocusHelperPath,"focusIcon.png")))
        if(len(email) == 0 and len(password) == 0):
            self.dialogBox.appendHtml(self.warningFormat.format("You didn't enter email or password!"))
            msgBox.setText("Please enter your email and password!")
            msgBox.exec()
        elif(len(email) == 0 and len(password) > 0):
            self.dialogBox.appendHtml(self.warningFormat.format("You didn't enter email!"))
            msgBox.setText("Please enter your email!")
            msgBox.exec()
        elif(len(email) > 0 and len(password) == 0):
            self.dialogBox.appendHtml(self.warningFormat.format("You didn't enter password!"))
            msgBox.setText("Please enter your password!")
            msgBox.exec()
        else: 
            valid = self.emailManage.emailValidator(email)
            print(valid)
            if (valid == 0):
                self.dialogBox.appendHtml(self.warningFormat.format("You entered an invalid email!"))
                msgBox.setText("Please enter a valid email!")
                msgBox.exec()
            elif (valid == 1):
                self.dialogBox.appendHtml(self.warningFormat.format("You entered a disposable email!"))
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
        elif(event.type() == QtCore.QEvent.ContextMenu and source is self.webList):
            menu = QMenu()
            unblockAction = menu.addAction("Unblock")
            try:
                chosenWeb = source.itemAt(event.pos()).text()
                action = menu.exec_(event.globalPos())
                if action != None:
                    if (action == unblockAction):
                        print("unblock")
                        chosenEmail = self.emailManage.getChosenEmail() 
                        if chosenEmail not in [None,"", " "]:
                            self.passwordPrompt(self.emailManage.getChosenEmail(),5,chosenWeb)
            except:
                print("exception happens")
        return super(UI,self).eventFilter(source, event)
    
    def passwordPrompt(self,email,actionType,chosenWeb=None):
        dlg =  QtWidgets.QInputDialog(self)          
        dlg.setInputMode(QtWidgets.QInputDialog.TextInput) 
        dlg.setLabelText("Please Enter Password:")   
        dlg.setFixedSize(350,100)              
        dlg.setWindowTitle("PASSWORD")       
        dlg.setWindowIcon(QIcon(os.path.join(FocusHelperPath,"focusIcon.png")))
        dlg.exec_()   
        #self.emailManage.passwordVerifier(email,dlg.textValue())
        passwordReturn = self.emailManage.passwordVerifier(email,dlg.textValue())
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle("WARNING")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setWindowIcon(QIcon(os.path.join(FocusHelperPath,"focusIcon.png")))
        if actionType == 0:
            if passwordReturn == 0:
                msgBox.setText("Wrong/No Password")
                msgBox.exec()
            else:
                self.dialogBox.appendHtml(self.validFormat.format("You activated email sender"))
                self.emailManage.emailActivate(email)
                msgBox.setText("Email Activated")
                msgBox.exec()
        elif actionType == 1: 
            if passwordReturn == 0:
                msgBox.setText("Wrong/No Password")
                msgBox.exec()
            else:
                self.dialogBox.appendHtml(self.warningFormat.format("You deleted an email!"))
                self.emailManage.deleteEmailFromDict(email)
                self.emailManage.rewriteEmailPasswordListAfterDelete()
                msgBox.setText("Email Deleted")
                msgBox.exec()
        elif actionType == 2:
            if passwordReturn == 0:
                msgBox.setText("Wrong/No Password")
                msgBox.exec()
            else:
                self.dialogBox.appendHtml(self.errorFormat.format("You deactivated email sender!"))
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
                self.dialogBox.appendHtml(self.warningFormat.format("You changed an email's password!"))
        elif actionType == 4:
            if passwordReturn == 0:
                msgBox.setText("Wrong/No Password")
                msgBox.exec()
            else:
                msgBox.setText("Quit already? I'm so disappointed in you!")
                msgBox.exec()
                self.webManage.emptyHostFile()
                subprocess.call(f"TASKKILL /F /T /IM FocusHelper.exe >nul 2>&1", shell=True)
        elif actionType == 5:
            if passwordReturn == 0:
                msgBox.setText("Wrong/No Password")
                msgBox.exec()
            else: 
                msgBox.setText("Unblock Successfully!\nRestart Browser to see effect")
                msgBox.exec()
                self.webManage.removeWebFromBlockedList(chosenWeb)
                
    def closeEvent(self, event):
        appManage = appManager().getNumberOfOccupiedApps()
        webManage = self.webManage.getNumberOfBlockedWebs()
        print(appManage)
        if self.emailManage.getChosenEmail() not in [0,None,""]: 
            if (appManage != 0 or webManage != 0):
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Critical)
                msgBox.setWindowTitle("ALERT")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.setWindowIcon(QIcon(os.path.join(FocusHelperPath,"focusIcon.png")))
                if (self.quitAttempt < 3):
                    self.quitAttempt += 1
                    msgBox.setText(f"Cannot close. Applications/Webs under lock or timer!\n Quit attempts: {self.quitAttempt}")
                    msgBox.exec()
                    self.dialogBox.appendHtml(self.errorFormat.format("Don't try to close the program!"))
                    event.ignore()
                else: 
                    self.webManage.emptyHostFile()
                    msgBox.setText("Quit attempts exceed 3. Notifying Super User...")
                    msgBox.exec()
                    emailSender.emailSender(self.emailManage.getChosenEmail())
                    event.accept()
                    subprocess.call(f"TASKKILL /F /T /IM FocusHelper.exe >nul 2>&1", shell=True)
            else:
                self.webManage.emptyHostFile()
                event.accept()
                subprocess.call(f"TASKKILL /F /T /IM FocusHelper.exe >nul 2>&1", shell=True)
        else: 
            self.webManage.emptyHostFile()
            event.accept()
            subprocess.call(f"TASKKILL /F /T /IM FocusHelper.exe >nul 2>&1", shell=True)
    
    def forcedShutDown(self):
        email = self.emailManage.getChosenEmail()
        appInProcess = appManager().getNumberOfOccupiedApps()
        if email not in [None,"",0] and appInProcess > 0:
            self.passwordPrompt(email,4)
            
    def advancedModeUnhide(self):
        print("unhide??")
        self.dialogBox.appendHtml(self.validFormat.format("You opened Advanced Mode menu"))
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
                if items == []: #this is to take care of empty selected item
                    return
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
                self.dialogBox.appendHtml(self.validFormat.format("You put a timer on an app"))
                
                self.dateTime.setDateTime(QtCore.QDateTime.currentDateTime())
                self.timeStopChosen = False
                self.anAppChosenToStop = False
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setWindowTitle("WARNING")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.setWindowIcon(QIcon(os.path.join(FocusHelperPath,"focusIcon.png")))
                msgBox.setText("Cannot set lock or timer on 6+ applications!")
                msgBox.exec()
                self.dialogBox.appendHtml(self.warningFormat.format("Cannot set lock or timer on 6+ applications!"))
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("WARNING")
            msgBox.setWindowIcon(QIcon(os.path.join(FocusHelperPath,"focusIcon.png")))
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
                if items == []: #this is to take care of empty selected item
                    return
                print("in if locker??")
                for item in items:
                    self.appDetect1.addLockedAppList(item.text())
                self.appDetect1.updateListAppView()
                self.appDetect2.updateListAppView()
                
                #extract duration from slider
                duration = self.durationSetter.value() * 600    #duration in secconds
                
                self.appLock = appLocker(duration,self.listApps,self.listApps2)
                self.pool.start(self.appLock.countDownLockerActivate)
                self.dialogBox.appendHtml(self.validFormat.format("You put a lock on an app"))
                
                self.durationAlreadySet = False
                self.anAppChosenToLock = False
            else: 
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setWindowTitle("WARNING")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.setWindowIcon(QIcon(os.path.join(FocusHelperPath,"focusIcon.png")))
                msgBox.setText("Cannot set lock or timer on 6+ applications!")
                msgBox.exec()
                self.dialogBox.appendHtml(self.warningFormat.format("Cannot set lock or timer on 6+ applications!"))
        else: 
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("WARNING")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.setWindowIcon(QIcon(os.path.join(FocusHelperPath,"focusIcon.png")))
            if (self.anAppChosenToLock == False) and (self.durationAlreadySet == False):
                msgBox.setText("Please select a duration and an app")
            elif (self.anAppChosenToLock == True) and (self.durationAlreadySet == False):
                msgBox.setText("Please select a duration")
            else: 
                msgBox.setText("Please select an app")
            msgBox.exec()        
    ############################################################################################################################################################################
        
####################################################################Main Controller#############################################################################################
FocusUiUrl = "https://raw.githubusercontent.com/PatrickDuong3001/FocusHelper/master/resources/FocusUI.ui"
HomeCssUrl = "https://raw.githubusercontent.com/PatrickDuong3001/FocusHelper/master/resources/Home.css"
HomeHtmlUrl = "https://raw.githubusercontent.com/PatrickDuong3001/FocusHelper/master/resources/Home.html"
StyleCssUrl = "https://raw.githubusercontent.com/PatrickDuong3001/FocusHelper/master/resources/Style.css"
StyleJsUrl = "https://raw.githubusercontent.com/PatrickDuong3001/FocusHelper/master/resources/Style.js"
FocusIcon1Url = "https://raw.githubusercontent.com/PatrickDuong3001/FocusHelper/master/resources/focusIcon.png"
FocusIcon2Url = "https://raw.githubusercontent.com/PatrickDuong3001/FocusHelper/master/resources/focusIcon2.png"
JQueryUrl = "https://raw.githubusercontent.com/PatrickDuong3001/FocusHelper/master/resources/jquery.js"
MediaUrl = "https://raw.githubusercontent.com/PatrickDuong3001/FocusHelper/master/resources/media.png"
UniversityUrl = "https://raw.githubusercontent.com/PatrickDuong3001/FocusHelper/master/resources/university.png"
appDataPath = os.getenv('LOCALAPPDATA')
FocusHelperPath = os.path.join(appDataPath,"FocusHelper")
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    if not os.path.exists(FocusHelperPath):
        os.mkdir(FocusHelperPath)
        wget.download(FocusUiUrl, os.path.join(FocusHelperPath,"FocusUI.ui"))
        wget.download(HomeCssUrl, os.path.join(FocusHelperPath,"Home.css"))
        wget.download(HomeHtmlUrl,os.path.join(FocusHelperPath,"Home.html"))
        wget.download(StyleCssUrl,os.path.join(FocusHelperPath,"Style.css"))
        wget.download(StyleJsUrl,os.path.join(FocusHelperPath,"Style.js"))
        wget.download(FocusIcon1Url,os.path.join(FocusHelperPath,"focusIcon.png"))
        wget.download(FocusIcon2Url,os.path.join(FocusHelperPath,"focusIcon2.png"))
        wget.download(JQueryUrl,os.path.join(FocusHelperPath,"jquery.js"))
        wget.download(MediaUrl,os.path.join(FocusHelperPath,"media.png"))
        wget.download(UniversityUrl,os.path.join(FocusHelperPath,"university.png"))
        time.sleep(3)
    app = QApplication(sys.argv)
    UIWindow = UI()
    sys.exit(app.exec()) 
else: 
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv[1:]), None, 1)