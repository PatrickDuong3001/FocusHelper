from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit
from PyQt5 import uic
import sys
import os

class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        uic.loadUi("FocusUI.ui",self)
        self.show() 
        
# Initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_() 