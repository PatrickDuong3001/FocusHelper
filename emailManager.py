from PyQt5.QtWidgets import QListWidgetItem
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import os
import re
import is_disposable_email
from os.path import exists
from configparser import ConfigParser

emailsDisplayed = []
class emailManager():
    def __init__(self,emailList):   
        super().__init__()
        self.emailList = emailList
        self.config = ConfigParser()
        self.config.read("resources/emailList.cfg")
        
    
    def setupFile(self):
        #prepare a config file 
        if(exists("resources/emailList.cfg") == False):
            f = open("resources/emailList.cfg","x")
            self.config.add_section("emails")
            self.config.add_section("passwords") 
            self.config.add_section("current_email")
            self.config.add_section("current_password")
            self.config.add_section("emailer_enable")
            self.config.add_section("chosen_email")
            with open("resources/emailList.cfg","w") as configfile:
                self.config.write(configfile)
        else: 
            self.emailListOnStart()
            self.displayEmailList(1)
    
    def emailValidator(self,email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, email)): 
            if(is_disposable_email.check(email) == False):
                return 2    #valid and non-disposable email
            else: 
                return 1
        else:
            return 0   
        
    def saveEmails(self,email):
        if (email in emailsDisplayed):
            pass
        else:
            emailIndex = self.countEmails()+1
            self.config.set("emails",f"email_{emailIndex}",email) 
            with open("resources/emailList.cfg","w") as configfile:
                self.config.write(configfile)
            self.addToEmailDisplayedList(email)
    
    def emailListOnStart(self):
        for (key, val) in self.getEmails():
            self.addToEmailDisplayedList(val)
        
    def displayEmailList(self,onStart=None):
        print(emailsDisplayed)
        if (onStart == None):
            self.emailList.clear()
            for (key, val) in self.getEmails():
                item = QListWidgetItem()
                item.setText(val)
                self.emailList.addItem(item)
        else:
            for (key, val) in self.getEmails():
                item = QListWidgetItem()
                item.setText(val)
                self.emailList.addItem(item)
        
    def countEmails(self):
        return self.config.items("emails").__len__()
        
    def getEmails(self):
        return self.config.items("emails")

    def setChosenEmail(self,email):
        self.config.set("chosen_email","email",email) 
        with open("resources/emailList.cfg","w") as configfile:
            self.config.write(configfile)
    
    def getEmailEnableStatus(self):
        for (key, val) in self.config.items("emailer_enable"):
            return val
    
    def setEmailEnableStatus(self,option):
        if (option == 1):
            self.config.set("emailer_enable","enabled","1") 
            with open("resources/emailList.cfg","w") as configfile:
                self.config.write(configfile)
        else:
            self.config.set("emailer_enable","enabled","0") 
            with open("resources/emailList.cfg","w") as configfile:
                self.config.write(configfile)
    
    def addToEmailDisplayedList(self,email):
        emailsDisplayed.append(email)
                
        #if timedAppList != None and itemToAdd in timedAppList:
        #   item.setFlags(Qt.NoItemFlags)
