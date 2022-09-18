from PyQt5.QtWidgets import QListWidgetItem
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import os
import re
import is_disposable_email

class emailManager():
    def __init__(self,emailInsert,passInsert,emailList):   
        super().__init__()
        self.emailInsert = emailInsert
        self.passInsert = passInsert
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
         
