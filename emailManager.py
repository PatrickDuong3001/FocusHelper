from PyQt5.QtWidgets import QListWidgetItem
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import os
import re
import is_disposable_email
from os.path import exists
from configparser import ConfigParser
import time
from PyQt5.QtGui import QColor

emailsDisplayedDict = {}
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
            self.config.add_section("chosen_email")
            with open("resources/emailList.cfg","w") as configfile:
                self.config.write(configfile)
        else: 
            self.emailListOnStart()
            self.displayEmailList(1)
            chosen_email = self.getChosenEmail()
    
    def emailValidator(self,email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, email)): 
            if(is_disposable_email.check(email) == False):
                return 2    #valid and non-disposable email
            else: 
                return 1
        else:
            return 0   
        
    def saveEmails(self,email,password):
        if (email in emailsDisplayedDict):
            pass
        else:
            emailIndex = self.countEmails()+1
            self.config.set("emails",f"email_{emailIndex}",email) 
            with open("resources/emailList.cfg","w") as configfile:
                self.config.write(configfile)
            self.savePasswords(emailIndex,password)
            self.addToEmailDisplayedDict(email,password)
    
    def savePasswords(self,index,password):
        self.config.set("passwords",f"pass_{index}",password) 
        with open("resources/emailList.cfg","w") as configfile:
            self.config.write(configfile)
    
    def emailListOnStart(self):
        tempForEmails = []
        i = 0
        for (key, val) in self.getEmails():
            self.addToEmailDisplayedDict(val,None)
            tempForEmails.append(val)
        for(key,val) in self.getPasswords():
            self.addToEmailDisplayedDict(tempForEmails[i],val)
            i+=1
        
    def displayEmailList(self,onStart=None):
        print(emailsDisplayedDict)
        if (onStart == None):
            self.emailList.clear()
            for (key, val) in self.getEmails():
                item = QListWidgetItem()
                item.setText(val)
                if val == self.getChosenEmail():
                    item.setBackground(QColor("#f0027f"))
                self.emailList.addItem(item)
        else:
            for (key, val) in self.getEmails():
                item = QListWidgetItem()
                item.setText(val)
                if val == self.getChosenEmail():
                    item.setBackground(QColor("#f0027f"))
                self.emailList.addItem(item)
        
    def countEmails(self):
        return self.config.items("emails").__len__()
        
    def getEmails(self):
        return self.config.items("emails")
    
    def getPasswords(self):
        return self.config.items("passwords")

    def emailActivate(self,email):
        self.setChosenEmail(email)
        self.displayEmailList()
    
    def setChosenEmail(self,email):
        self.config.set("chosen_email","email",email) 
        with open("resources/emailList.cfg","w") as configfile:
            self.config.write(configfile)
    
    def addToEmailDisplayedDict(self,email,password):
        emailsDisplayedDict[email] = password
    
    def passwordVerifier(self,email,password):
        if password == emailsDisplayedDict[email]:
            return 1
        return 0

    def getChosenEmail(self):
        for (key, val) in self.config.items("chosen_email"):
            return val
        
    def rewriteEmailPasswordListAfterDelete(self):
        self.config.remove_section("emails")
        self.config.remove_section("passwords")
        time.sleep(0.5)
        self.config.add_section("emails")
        self.config.add_section("passwords")
        i = 1
        j = 1
        for email in emailsDisplayedDict:
            self.config.set("emails",f"email_{i}",email)
            i += 1
        for email,password in emailsDisplayedDict.items():
            self.config.set("passwords",f"pass_{j}",password)
            j += 1
        with open("resources/emailList.cfg","w") as configfile:
            self.config.write(configfile)
        self.displayEmailList()
    
    def deleteChosenEmail(self):
        self.config.remove_section("chosen_email")
        time.sleep(0.5)
        self.config.add_section("chosen_email")
        with open("resources/emailList.cfg","w") as configfile:
            self.config.write(configfile)
        self.displayEmailList()
            
    def changeEmailPassword(self,email,newPassword):
        self.changeEmailPasswordinDict(email,newPassword)
        self.rewriteEmailPasswordListAfterDelete()
        
    def changeEmailPasswordinDict(self,email,newPassword):
        emailsDisplayedDict[email] = newPassword
    
    def deleteEmailFromDict(self,email):
        emailsDisplayedDict.pop(email)
        print(emailsDisplayedDict)
        #have to rewrite the whole "emails" section in emailList.cfg since the index of deleted email is randomly specified by user
        
    
