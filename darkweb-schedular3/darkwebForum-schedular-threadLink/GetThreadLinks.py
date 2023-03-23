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
from Login import detect_login,login_button_detect
import undetected_chromedriver as uc

        
def addingToDB(data):
    collection2.insert_many(data)

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
     
# functions for dataTime--------------------

def clndate(date,date_formats):
    try:
        
        result = re.search(r"^[A-Za-z]+\s\d{1,2},\s\d{4},\s\d{2}:\d{2}\s[A-Z]{2}", date).group()
        for date_format in date_formats:
            try:
                date_object = datetime.strptime(result, date_format)
                # new_format = "%d-%m-%Y"
                new_format="%Y-%m-%d %H:%M:%S"
                new_date_string = date_object.strftime(new_format)
                # print(new_date_string)
                return new_date_string
            except:
                pass

    except:
        pass

def date_formating(date_string):
    date_formats = [ '%Y-%m-%d %H:%M:%S', '%Y-%m-%d','%m-%d-%Y', '%Y/%m/%d,%H:%M:%S', '%d-%m-%Y','%d-%m-%Y,%H:%M:%S','%m-%d-%Y,%H:%M:%S', '%d-%m-%Y %H:%M:%S', '%B %d, %Y, %I:%M %p', '%b %d, %Y, %I:%M %p', '%Y%m%dT%H%M%S.%fZ', '%Y%m%dT%H%M%S.%f%z', '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%S.%f%z', '%Y-%m-%dT%H:%M:%S.%f', '%Y/%m/%d', '%d.%m.%Y', '%d.%m.%Y %H:%M:%S', '%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M', '%d/%m/%y %H:%M:%S', '%d/%m/%y %H:%M', '%m/%d/%Y %H:%M:%S', '%m/%d/%Y %I:%M:%S %p', '%m/%d/%Y %I:%M %p', '%m/%d/%y %I:%M:%S %p', '%m/%d/%y %I:%M %p', '%d %B %Y', '%d %b %Y', '%d %B %y', '%d %b %y', '%d,%m,%Y,%I:%M %p', '%m,%d,%Y,%I:%M:%S %p', '%Y,%m,%d,%H:%M:%S', '%m,%d,%y,%I:%M:%S %p', '%d,%b,%Y,%I:%M %p', '%d/%m/%Y %H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%S.%f%z','%m-%d-%Y, %I:%M %p']
    for date_format in date_formats:
        try:
            date_object = datetime.strptime(date_string, date_format)
            new_format="%Y-%m-%d %H:%M:%S"
            new_date_string = date_object.strftime(new_format)
            return new_date_string
        except :
            try:
                new_date_string = clndate(date_string,date_formats)
                if new_date_string:
                    return new_date_string
            except:
                pass  
                        
            #Today with hrs
            try:      
                match = re.search("(\d+) hours", date_string) or re.search("(\d+) Hours", date_string) or re.search("(\d+) hrs", date_string) or re.search("(\d+) Hrs", date_string) or re.search("(\d+) hrs.", date_string) or re.search("(\d+) Hrs.", date_string) or re.search("Today,(\d+) hours", date_string) or re.search("Today,(\d+) Hours", date_string) or re.search("Today,(\d+) hrs", date_string) or re.search("Today,(\d+) Hrs", date_string) or re.search("Today,(\d+) hrs.", date_string) or re.search("Today,(\d+) Hrs.", date_string)  or re.search("today,(\d+) hours", date_string) or re.search("today,(\d+) Hours", date_string) or re.search("today,(\d+) hrs", date_string) or re.search("today,(\d+) Hrs", date_string) or re.search("today,(\d+) hrs.", date_string) or re.search("today,(\d+) Hrs.", date_string)
                if match:
                    hours = int(match.group(1))
                else:
                    raise ValueError("Invalid date string format")
                now = datetime.now()
                date_object = now - timedelta(hours=hours)

                new_format="%Y-%m-%d %H:%M:%S"
                new_date_string = date_object.strftime(new_format)
                return new_date_string
            except:
                pass
            
            #Days (25 Days ago)
            try:      
                match = re.search("(\d+) days", date_string) or re.search("(\d+) Days", date_string) or re.search("(\d+) day", date_string) or re.search("(\d+) Day", date_string) or re.search("(\d+) hrs.", date_string) 
                if match:
                    days = int(match.group(1))
                else:
                    raise ValueError("Invalid date string format")
                now = datetime.now()
                date_object = now - timedelta(days=days)

                new_format="%Y-%m-%d %H:%M:%S"
                new_date_string = date_object.strftime(new_format)
                return new_date_string
            except:
                pass
            
            #Days (25 months ago)
            try:      
                match = re.search("(\d+) month", date_string) or re.search("(\d+) Month", date_string) or re.search("(\d+) months ago", date_string) or re.search("(\d+) Months", date_string) 
                if match:
                    months= int(match.group(1))
                else:
                    raise ValueError("Invalid date string format")
                now = datetime.now()
                date_object = now - timedelta(30*months)

                new_format="%Y-%m-%d %H:%M:%S"
                new_date_string = date_object.strftime(new_format)
                return new_date_string
            except:
                pass
                               
            # today with minutes              
            try:      
                match = re.search("(\d+) minutes", date_string) or re.search("(\d+) Minutes", date_string) or re.search("(\d+) min", date_string) or re.search("(\d+) Min", date_string) or re.search("(\d+) min.", date_string) or re.search("(\d+) Min.", date_string) or re.search("Today,(\d+) minutes", date_string) or re.search("Today,(\d+) Minutes", date_string) or re.search("Today,(\d+) min", date_string) or re.search("Today,(\d+) Min", date_string) or re.search("Today,(\d+) min.", date_string) or re.search("Today,(\d+) Min.", date_string)  or re.search("today,(\d+) minutes", date_string) or re.search("today,(\d+) Minutes", date_string) or re.search("today,(\d+) min", date_string) or re.search("today,(\d+) Min", date_string) or re.search("today,(\d+) min.", date_string) or re.search("today,(\d+) Min.", date_string)
                if match:
                    minutes = int(match.group(1))
                else:
                    raise ValueError("Invalid date string format")
                now = datetime.now()
                date_object = now - timedelta(minutes=minutes)

                new_format="%Y-%m-%d %H:%M:%S"
                new_date_string = date_object.strftime(new_format)
                return new_date_string
            except:
                pass
            
            # Seconds ago
            try:      
                match = re.search("(\d+) seconds", date_string) or re.search("(\d+) Seconds", date_string) or re.search("(\d+) sec", date_string) or re.search("(\d+) Sec", date_string) or re.search("(\d+) sec.", date_string) or re.search("(\d+) Sec.", date_string)
                if match:
                    second = int(match.group(1))
                else:
                    raise ValueError("Invalid date string format")
                now = datetime.now()
                date_object = now - timedelta(seconds=second)

                new_format="%Y-%m-%d %H:%M:%S"
                new_date_string = date_object.strftime(new_format)
                return new_date_string
            except:
                pass
            
            # Seconds ago
            try:      
                match = re.search("(\d+) year", date_string) or re.search("(\d+) Year", date_string) or re.search("(\d+) yrs", date_string) or re.search("(\d+) Yrs", date_string) or re.search("(\d+) yrs.", date_string) or re.search("(\d+) Yrs.", date_string)
                if match:
                    years = int(match.group(1))
                else:
                    raise ValueError("Invalid date string format")
                now = datetime.now()
                date_object = now - timedelta(365*years)

                new_format="%Y-%m-%d %H:%M:%S"
                new_date_string = date_object.strftime(new_format)
                return new_date_string
            except:
                pass
            
            # week ago
            try:      
                match = re.search("(\d+) week", date_string) or re.search("(\d+) Week", date_string) or re.search("(\d+) weeks", date_string) or re.search("(\d+) Weeks", date_string) 
                if match:
                    week = int(match.group(1))
                else:
                    raise ValueError("Invalid date string format")
                now = datetime.now()
                date_object = now - timedelta(7*week)

                new_format="%Y-%m-%d %H:%M:%S"
                new_date_string = date_object.strftime(new_format)
                return new_date_string
            except:
                pass

def date_coverter(input_date):
    try:
        output = date_formating(input_date)
        dt = datetime.strptime(output, "%Y-%m-%d %H:%M:%S")
        timestamp = dt.timestamp()
        return int(timestamp)
    except:
        try:
            if ('today' in input_date.lower()) or ('hours' in input_date.lower()) or ('hour' in input_date.lower()) or ('minutes' in input_date.lower()) or ('min' in input_date.lower()):
                current_GMT = time.gmtime()
                ts = calendar.timegm(current_GMT)
                return str(int(ts))
        except:
            pass

def getThreadLinks(siteLink,sectionPath,urlPath,lastModPath,path_of_next_btn):
    with TorBrowserDriver(torPath) as driver:
        # driver.get(siteLink)
        # driver =uc.Chrome()
    # wordList=['hack','High Quality','Anime Clicker Fight']
        try:
            driver.get(siteLink)
            time.sleep(2)
            detect_login(driver, siteLink)
        except:
            pass
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

        for _ in range(min(len(threadLinks),len(lastModDates))):
            dct={'title':threadTitles[_],'url':threadLinks[_],'lastModDate':lastModDates[_],'isUrgent':False,'status':None,"failedCount":0,'time':datetime.now() }
            print(dct)
            allData.append(dct)
        # return allData
        addingToDB(allData)






        if len(threadLinks)==0:
            CurrUrl,driver =login_button_detect(driver,siteLink)
            driver,currentUrl=detect_login(driver,CurrUrl)
            try:
                driver.get(currentUrl)
                time.sleep(2)
                # detect_login(driver, siteLink)
            except:
                pass
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

            for _ in range(min(len(threadLinks),len(lastModDates))):
                dct={'title':threadTitles[_],'url':threadLinks[_],'lastModDate':lastModDates[_],'isUrgent':False,'status':None,"failedCount":0,'time':datetime.now() }
                print(dct)
                allData.append(dct)
            # return allData
            addingToDB(allData)






# site='https://corsair.wtf/'
# sectionPath=[['CSS_SELECTOR','#ipsLayout_mainArea > section > ol > li:nth-child(1) > ol > li:nth-child(3) > div.ipsDataItem_main > h4 > a']] 
# urlPath=['CSS_SELECTOR','span.ipsType_break.ipsContained >a']
# lastModPath=['CSS_SELECTOR',' li > div > div > time']
# path_of_sectionNext_btn=['CSS_SELECTOR','li.ipsPagination_next>']

# print(getThreadLinks(site,sectionPath,urlPath,lastModPath,path_of_sectionNext_btn))
