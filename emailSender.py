import smtplib
import time
 

class emailSender():
    '''
    this class put a lock on an app
    the class adopts multithreading model
    '''
    def __init__(self):   
        super().__init__()
        self.sendEmail = smtplib.SMTP('smtp.gmail.com', 587) # creates SMTP session
        self.sendEmail.starttls() # start TLS for security
        self.sendEmail.login("focushelperadm@gmail.com", "iccrdzkaerxehsgz") # Authentication
        
        self.currentHour = time.strftime("%H", time.localtime())       
        self.currentMin = time.strftime("%M", time.localtime())
        
        self.subject = "IMPORTANT: Unauthorized termination of program detected"
        self.text = f"The system detected several attempts to close FocusHelper at {self.currentHour}:{self.currentMin}"
        self.message = 'Subject: {}\n\n{}'.format(self.subject, self.text) # message to be sent
        
        self.sendEmail.sendmail("focushelperadm@gmail.com", "baophuc2000@gmail.com", self.message,"1") # sending the mail
        self.sendEmail.quit() # terminating the session

emailSender()