from PyQt5.QtWidgets import QListWidgetItem
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import os
import re
from os.path import exists
from configparser import ConfigParser
import time
from PyQt5.QtGui import QColor

displayedWeb = []
class websiteManager():
    def __init__(self,webList):   
        super().__init__()
        self.webList = webList
        self.config = ConfigParser()
        self.config.read("resources/webList.cfg")
        
    def fileHandler(self):
        #prepare a config file 
        if(exists("resources/webList.cfg") == False):
            f = open("resources/webList.cfg","x")
            self.config.add_section("websites")
            with open("resources/webList.cfg","w") as configfile:
                self.config.write(configfile)
        else: 
            print()