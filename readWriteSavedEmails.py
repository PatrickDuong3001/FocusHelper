from configparser import ConfigParser

class readWriteSavedEmails():
    '''
    this class help save email list and password
    '''
    def __init__(self):   
        super().__init__()
        self.config = ConfigParser()
        self.config.read("resources/emailList.cfg")
    
    def countEmails(self):
        return self.config.items("emails").__len__()
    
    def writeEmail(self,email):
        print("inside writeEmail??")
        emailIndex = self.countEmails()+1
        self.config.set("emails",f"email_{emailIndex}",email) 
        with open("resources/emailList.cfg","w") as configfile:
            self.config.write(configfile)
            
#readWriteFile = readWriteSavedEmails()
#readWriteFile.writeEmail("baophuc2000@gmail.com")