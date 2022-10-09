#!python
# coding: utf-8
import ctypes, sys
import time
import ctypes, sys
from datetime import datetime as dt
#Windows host file path
hosts_path=r"C:\Windows\System32\drivers\etc\hosts"
#test_path = r"C:\Windows\System32\drivers\etc\something"
redirect="127.0.0.1"
#Add the website you want to block, in this list
websites=["www.youtube.com","youtube.com", "www.facebook.com", "facebook.com"]
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    # Code of your program here
    while True:
    # time of your work
        if 9 < 10:
            print("Working hours...")
            with open(hosts_path, 'r+') as file:
                content = file.read()
                for website in websites:
                    if website in content:
                        pass
                    else:
                        # mapping hostnames to your localhost IP address
                        file.write(redirect + " " + website + "\n")
        else:
            with open(hosts_path, 'r+') as file:
                content=file.readlines()
                file.seek(0)
                for line in content:
                    if not any(website in line for website in websites):
                        file.write(line)
                # removing hostnmes from host file
                file.truncate() 
            print("Fun hours...")
        time.sleep(5)    
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    #f = open(test_path,"x") create file with no extensions
    