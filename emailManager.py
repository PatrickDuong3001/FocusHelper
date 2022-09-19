from PyQt5.QtWidgets import QListWidgetItem
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import os
import re
import is_disposable_email
import readWriteSavedEmails

class emailManager():
    def __init__(self,emailList):   
        super().__init__()
        self.fileWriter = readWriteSavedEmails.readWriteSavedEmails()
        self.emailList = emailList
        
    
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
        print("inside saveEmails??")
        self.fileWriter.writeEmail(email)
