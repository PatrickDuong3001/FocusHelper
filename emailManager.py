from PyQt5.QtWidgets import QListWidgetItem
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import os
import re
import is_disposable_email
from os.path import exists
from configparser import ConfigParser

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
            self.config.add_section("current_email")
            self.config.add_section("current_password")
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
    
    def getPasswords(self):
        return self.config.items("passwords")

    def setChosenEmail(self,email):
        self.config.set("chosen_email","email",email) 
        with open("resources/emailList.cfg","w") as configfile:
            self.config.write(configfile)
    
    def addToEmailDisplayedDict(self,email,password):
        emailsDisplayedDict[email] = password
    
    def passwordVerifier(self,email,password):
        if password == emailsDisplayedDict[email]:
            self.setChosenEmail(email)
            return 1
        return 0

    def getChosenEmail(self):
        for (key, val) in self.config.items("chosen_email"):
            return val
    
    def deleteEmailFromDict(self,email):
        emailsDisplayedDict.pop(email)
        #have to rewrite the whole "emails" section in emailList.cfg since the index of deleted email is randomly specified by user
        
    
