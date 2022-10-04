from PyQt5 import QtTest

class customTimer():
    '''
    this class is used to pause the program 
    '''
    def __init__(self,duration=1000,dialogBox=None,msg=None,final_msg=None):   
        super().__init__()
        if dialogBox == None:
            QtTest.QTest.qWait(duration)
        else:
            self.message = "" if msg == None else msg
            self.dialogBox = dialogBox

            
            self.dialogBox.appendPlainText(msg)
            QtTest.QTest.qWait(duration)
            self.dialogBox.appendPlainText(final_msg)
            