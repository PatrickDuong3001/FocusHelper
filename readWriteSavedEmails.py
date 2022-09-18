from configparser import ConfigParser
from os.path import exists

class readWriteSavedEmails():
    '''
    this class help save email list and password
    '''
    def __init__(self):   
        super().__init__()
        self.config = ConfigParser()
        self.config.read("resources/emailList.cfg")
    
    
readWriteFile = readWriteSavedEmails()