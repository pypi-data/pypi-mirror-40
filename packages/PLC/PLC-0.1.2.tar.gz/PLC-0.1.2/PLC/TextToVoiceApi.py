from selenium import webdriver
import time
from PLC.AudioTools import DownloadBlob
from PLC.TextTools import RemoveSpaces
def CreateBrowser():
    try:
        browser = webdriver.Chrome()
    except:
        browser = webdriver.Chrome(executable_path='C:\chromedriver.exe')
    browser.get('https://www.naturalreaders.com/online/')
    return browser
def ConvertTextToVoice(Name, Text, Speed=1, browser=None, browserRemainOpen=False):
    if browser == None:
        browser = CreateBrowser()
    Byte = b''
    currentName = GetCurrentName(browser)
    if Name!=currentName:
        ChangeName(Name, browser)
    currentSpeed = GetCurrentSpeed(browser)
    if Speed != currentSpeed:
        ChangeSpeed(Speed, browser)
    Text = RemoveSpaces(Text, addDot=False)
    for Sentence in Text.split("."):
        for Sen in Sentence.split("?"):
            for Se in Sen.split("!"):
                Byte += Get(Se, browser)
    if not browserRemainOpen:
        browser.quit()
    return Byte
def GetCurrentName(browser=None):
    if browser == None:
        browser = CreateBrowser()
    Name = browser.find_element_by_id('chooseVoice').text
    return Name
def GetCurrentSpeed(browser=None):
    if browser == None:
        browser = CreateBrowser()
    Speed = browser.find_element_by_id('selectedSpeed').text
    return Speed
def Get(text, browser):

    Text = browser.find_element_by_id('inputDiv')
    Cleared = Text.text == ''
    try:
        TextClear = browser.find_elements_by_class_name('btnClose')[0]
        TextClear.click()
    except:
        while not Cleared:
            try:
                Text.clear()
                Cleared = True
            except:
                time.sleep(0.1)
    Text.send_keys(text)
    PageSource = browser.page_source
    Found = 'src' in PageSource.split('<audio id="audio" controls="controls"')[1].split('>')[0]
    if Found:
        PreAudioSrc = PageSource.split('<audio id="audio" controls="controls" src="')[1].split('">')[0]
    else:
        PreAudioSrc = ''
    Button = browser.find_element_by_class_name("playPause")
    Button.click()

    Found = False
    while not Found:
        time.sleep(0.1)
        PageSource = browser.page_source
        Found = 'src' in PageSource.split('<audio id="audio" controls="controls"')[1].split('>')[0]
        if Found:
            AudioSrc = PageSource.split('<audio id="audio" controls="controls" src="')[1].split('">')[0]#.split("blob:")[1]
            if AudioSrc == PreAudioSrc:
                Found = not Found

    Bytes1 = DownloadBlob(browser, AudioSrc)
    return Bytes1
def ChangeName(Name, browser):
    SelectBtn = browser.find_element_by_id('chooseVoice')
    SelectBtn.click()

    F1 = browser.find_element_by_id("dropdownMenuvoicelist")
    F2 = F1.find_element_by_class_name("languageContent")
    F3 = F2.find_element_by_class_name("tabContainer")
    F4 = F3.find_element_by_class_name("premiumContent")
    F5 = F4.find_element_by_id("onlinecontent")
    F6 = F5.find_element_by_class_name("content")
    ul = F6.find_element_by_tag_name("ul")
    li_s = ul.find_elements_by_tag_name('li')

    for li in li_s:
        NameDiv = li.find_element_by_class_name("personName")
        if NameDiv.text == Name:
            li.click()
            break
def ChangeSpeed(Speed, browser):
    SelectBtn = browser.find_element_by_class_name('selectedSpeed')
    SelectBtn.click()

    F1 = browser.find_element_by_id("dropdownMenu")
    ul = F1.find_element_by_tag_name("ul")
    li_s = ul.find_elements_by_tag_name('li')

    for li in li_s:
        SpeedLi = li.text
        if SpeedLi.text == Speed:
            li.click()
            break
