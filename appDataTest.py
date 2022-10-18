import os
import wget
import time

FocusUiUrl = "https://raw.githubusercontent.com/PatrickDuong3001/FocusHelper/master/resources/FocusUI.ui"
HomeCssUrl = "https://raw.githubusercontent.com/PatrickDuong3001/FocusHelper/master/resources/Home.css"
HomeHtmlUrl = "https://raw.githubusercontent.com/PatrickDuong3001/FocusHelper/master/resources/Home.html"
StyleCssUrl = "https://raw.githubusercontent.com/PatrickDuong3001/FocusHelper/master/resources/Style.css"
StyleJsUrl = "https://raw.githubusercontent.com/PatrickDuong3001/FocusHelper/master/resources/Style.js"
FocusIcon1Url = "https://raw.githubusercontent.com/PatrickDuong3001/FocusHelper/master/resources/focusIcon.png"
FocusIcon2Url = "https://raw.githubusercontent.com/PatrickDuong3001/FocusHelper/master/resources/focusIcon2.png"
JQueryUrl = "https://raw.githubusercontent.com/PatrickDuong3001/FocusHelper/master/resources/jquery.js"
MediaUrl = "https://raw.githubusercontent.com/PatrickDuong3001/FocusHelper/master/resources/media.png"
UniversityUrl = "https://raw.githubusercontent.com/PatrickDuong3001/FocusHelper/master/resources/university.png"

appDataPath = os.getenv('LOCALAPPDATA')
FocusHelperPath = os.path.join(appDataPath,"FocusHelper")
fileName = os.path.join(FocusHelperPath,"FocusUI.ui")

if not os.path.exists(FocusHelperPath):
    os.mkdir(FocusHelperPath)
    wget.download(FocusUiUrl, os.path.join(FocusHelperPath,"FocusUI.ui"))
    wget.download(HomeCssUrl, os.path.join(FocusHelperPath,"Home.css"))
    wget.download(HomeHtmlUrl,os.path.join(FocusHelperPath,"Home.html"))
    wget.download(StyleCssUrl,os.path.join(FocusHelperPath,"Style.css"))
    wget.download(StyleJsUrl,os.path.join(FocusHelperPath,"Style.js"))
    wget.download(FocusIcon1Url,os.path.join(FocusHelperPath,"focusIcon.png"))
    wget.download(FocusIcon2Url,os.path.join(FocusHelperPath,"focusIcon2.png"))
    wget.download(JQueryUrl,os.path.join(FocusHelperPath,"jquery.js"))
    wget.download(MediaUrl,os.path.join(FocusHelperPath,"media.png"))
    wget.download(UniversityUrl,os.path.join(FocusHelperPath,"university.png"))
    time.sleep(3)
    
