from PyQt5.QtWidgets import QListWidgetItem
import time
from os.path import exists

hosts_path=r"C:\Windows\System32\drivers\etc\hosts"
redirect="127.0.0.1"
blockedWebList = []
class websiteManager():
    def __init__(self,webList):   
        super().__init__()
        self.webList = webList
        if(exists(hosts_path) == False):         #check if there's already a hostfile
            f = open(hosts_path,"x")
                    
    def addToBlockedList(self,web):
        webUrl = None
        if "www." not in web:
            webUrl = "www." + web
            if webUrl not in blockedWebList:
                blockedWebList.append(webUrl)
        else:
            webUrl = web
            if webUrl not in blockedWebList:
                blockedWebList.append(webUrl)
        self.displayWebList()
        self.writeHostFile()
            
    def displayWebList(self):
        self.webList.clear()
        for web in blockedWebList:
            item = QListWidgetItem()
            item.setText(web)
            self.webList.addItem(item)
    
    def removeWebFromBlockedList(self,web):
        self.emptyHostFile()
        blockedWebList.remove(web)
        self.displayWebList()
        time.sleep(0.5)
        self.writeHostFile()
        
    def writeHostFile(self):
        with open(hosts_path, 'r+') as file:
            content = file.read()
            for website in blockedWebList:
                if website in content:
                    pass
                else:
                    # mapping hostnames to your localhost IP address
                    file.write(redirect + " " + website + "\n")
    
    def emptyHostFile(self):
        with open(hosts_path, 'r+') as file:
            file.truncate(0)
    
    def getNumberOfBlockedWebs(self):
        print(len(blockedWebList))
        return len(blockedWebList)