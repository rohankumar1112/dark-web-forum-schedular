from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium import webdriver
from datetime import datetime, timedelta
import re
from bs4 import BeautifulSoup
import pymongo
import time
from driverpath import torPath
from tbselenium.tbdriver import TorBrowserDriver
from databaseConnection import collection2
from WordLists import wordList
import calendar
from Login import detect_login,login_button_detect,login_fill
# import undetected_chromedriver as uc
from timestamp_convertor import date_coverter
from flag import sendLog,sendData
from startDisplay import *
        
def addingToDB(allData):
    for data in allData:
        url=data['url']
        check=collection2.find_one({"url": f"{url}"})
        if check:
            id=check['_id']
            db_lastModDate=check['lastModDate']
            data_lastModDate=data['lastModDate']
            if db_lastModDate!=data_lastModDate:
                q={'_id':id}
                collection2.delete_one(q)
                collection2.insert_one(data)
                print('DataBase Updated!!')
                # sendLog('DataBase Updated!!')
        else:
            collection2.insert_one(data)
            print("Adding New Data...")
            # sendLog("Adding New Data...")
            print("DataBase Updated!!")
            # sendLog("DataBase Updated!!")

def press_next_btn(driver,path_of_next_btn) :
    try :
        type,path = path_of_next_btn
        next_btn = driver.find_element(selector(type),path)
        if next_btn.is_enabled or next_btn.is_displayed  and not 'link-unactive' in next_btn.get_attribute('class') :
            driver.execute_script("arguments[0].scrollIntoView();", next_btn)
            link_of_next_page = next_btn.get_attribute("href")
            return link_of_next_page
        else:
            return False
        
    except NoSuchElementException:
        return False
    except ElementNotInteractableException:
        return False

def selector(type):
    if type=='XPATH':
        return By.XPATH
    elif(type=='CSS_SELECTOR'):
        return By.CSS_SELECTOR    
    elif(type=='ID'):
        return By.ID    
    elif(type=='CLASS_NAME')  :
        return By.CLASS_NAME  
    elif(type=='TAG_NAME'):
        return By.TAG_NAME
    else:
        print('Wrong path_type')
        # sendLog('Wrong path_type')
     
def getThreadLinks(siteLink,sectionPath,urlPath,lastModPath,path_of_next_btn):

    xvfb_display = start_xvfb()
    with TorBrowserDriver(torPath) as driver:
        # driver.get(siteLink)
        # driver =uc.Chrome()
        
        driver.get(siteLink)
        time.sleep(8)
        detect_login(driver, siteLink)

        allSectionLinks=[]
        for s in sectionPath:
            type,path = s
            sections=driver.find_elements(selector(type),path)
            try:
                for section in sections:
                    link=section.get_attribute('href')
                    allSectionLinks.append(link)
            except:
                pass
        Temp_threadLinks=[]
        Temp_lastModDates=[]
        
        threadTitles=[]
        threadLinks=[]
        lastModDates=[]
        
        allData=[]
        prev_url=None
        for link in allSectionLinks:
            
            try:
                driver.get(link)
                time.sleep(2)
            except:
                pass
            while True:
                
                type,path = lastModPath
                lastMods=driver.find_elements(selector(type),path)
                for lastMod in lastMods:
                    try:
                        lastModDate =lastMod.get_attribute('data-time')
                        if lastModDate==None:
                            element_html=lastMod.get_attribute('outerHTML')
                            lastModDate=BeautifulSoup(element_html,'html.parser')
                            lastModDate_text=lastModDate.text
                            try:
                                lastModDate=str(int(date_coverter(lastModDate_text)))
                                if lastModDate=='None':
                                    lastModDate=lastModDate_text
                            except:
                                lastModDate=lastModDate_text
                            
                        Temp_lastModDates.append(lastModDate)
                    except:
                        pass
                
                type,path = urlPath
                urls=driver.find_elements(selector(type),path)
                for u in urls:
                    element_html=u.get_attribute('outerHTML')
                    title=BeautifulSoup(element_html,'html.parser')
                    title=title.text
                    url=u.get_attribute('href')
                    Temp_threadLinks.append(url)
                    for word in wordList:
                        if word.lower() in title.lower():
                            url=u.get_attribute('href')
                            threadTitles.append(title)
                            threadLinks.append(url)
                            tempIndex=Temp_threadLinks.index(url)
                            lastModDates.append(Temp_lastModDates[tempIndex])
                            break
                try:
                    check=press_next_btn(driver,path_of_next_btn)
                    curr_url=check
                    if curr_url==prev_url:
                        break
                    else:
                        prev_url=curr_url
                    if check==False:
                        break
                    else:
                        driver.get(check)
                        time.sleep(1)
                except:
                    break




        if len(threadLinks)==0:
            url,driver2=login_button_detect(driver,siteLink)
            login_fill(driver)
            time.sleep(2)
            driver.get(siteLink)
            time.sleep(2)

            allSectionLinks=[]
            for s in sectionPath:
                type,path = s
                sections=driver.find_elements(selector(type),path)
                try:
                    for section in sections:
                        link=section.get_attribute('href')
                        allSectionLinks.append(link)
                except:
                    pass
            Temp_threadLinks=[]
            Temp_lastModDates=[]
            
            threadTitles=[]
            threadLinks=[]
            lastModDates=[]
            
            allData=[]
            prev_url=None
            for link in allSectionLinks:
                
                try:
                    driver.get(link)
                    time.sleep(2)
                except:
                    pass
                while True:
                    
                    type,path = lastModPath
                    lastMods=driver.find_elements(selector(type),path)
                    for lastMod in lastMods:
                        try:
                            lastModDate =lastMod.get_attribute('data-time')
                            if lastModDate==None:
                                element_html=lastMod.get_attribute('outerHTML')
                                lastModDate=BeautifulSoup(element_html,'html.parser')
                                lastModDate_text=lastModDate.text
                                try:
                                    lastModDate=str(int(date_coverter(lastModDate_text)))
                                    if lastModDate=='None':
                                        lastModDate=lastModDate_text
                                except:
                                    lastModDate=lastModDate_text
                                
                            Temp_lastModDates.append(lastModDate)
                        except:
                            pass
                    
                    type,path = urlPath
                    urls=driver.find_elements(selector(type),path)
                    for u in urls:
                        element_html=u.get_attribute('outerHTML')
                        title=BeautifulSoup(element_html,'html.parser')
                        title=title.text
                        url=u.get_attribute('href')
                        Temp_threadLinks.append(url)
                        for word in wordList:
                            if word.lower() in title.lower():
                                url=u.get_attribute('href')
                                threadTitles.append(title)
                                threadLinks.append(url)
                                tempIndex=Temp_threadLinks.index(url)
                                lastModDates.append(Temp_lastModDates[tempIndex])
                                break
                    try:
                        check=press_next_btn(driver,path_of_next_btn)
                        curr_url=check
                        if curr_url==prev_url:
                            break
                        else:
                            prev_url=curr_url
                        if check==False:
                            break
                        else:
                            driver.get(check)
                            time.sleep(1)
                    except:
                        break
        if len(threadLinks)==0:
            print('login or captcha |or Can not find links with matching word list!!')
            return False
        for _ in range(min(len(threadLinks),len(lastModDates))):
            dct={'title':threadTitles[_],'url':threadLinks[_],'lastModDate':lastModDates[_],'isUrgent':False,'status':None,"failedCount":0,'time':datetime.now()}
            print(dct)
            # sendData(dct)
            allData.append(dct)
        addingToDB(allData)
    stop_xvfb(xvfb_display)





        





