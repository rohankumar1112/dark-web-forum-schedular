from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium import webdriver
from datetime import datetime, timedelta
import re
from bs4 import BeautifulSoup
import pymongo
from statusHandler import *
import time
import calendar
from Login import detect_login
from driverpath import torPath
from databaseConnection import *
# client=pymongo.MongoClient('mongodb://localhost:27017/')
# db=client['automation']
# collection=db['1']


        
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

def forum_scrap(threadUrls,lastModDate,title_path,iterator_path,author_name_path,profile_link_path,date_path,body_path,media_path,path_of_next_btn,expand_btn=[None,None],failedCount=0):  
    
    driver = webdriver.Chrome('chromedriver.exe')
    
    for p in range(min(len(threadUrls),len(lastModDate))):
        url=threadUrls[p]    
        try:
            print(url,"is Scrapping now...")
            # sendLog(url,"is Scrapping now...")
            scrapRunning(url)
            driver.get(url)
            time.sleep(1)
            detect_login(driver,url)
            
        except:
            print("not Scrapped!!---->",url)
            # sendLog("not Scrapped!!---->",url) #test 3
            print("FailedCount is:",str(int(failedCount)+1))
            # sendLog("FailedCount is:",str(failedCount+1))  #test 2
            scrapFailed(url,int(failedCount)) 
            isNodeBusy =False
            
        try:      
            type,path =title_path
            title=driver.find_element(selector(type),str(path))
            element_html=title.get_attribute('outerHTML')
            title=BeautifulSoup(element_html,'html.parser')
            title=title.text
        except:   
            title='not found'

        allPosts=[]
        prev_url=None
        if title  !='not found':
            

            while True:
                type,path = iterator_path
                iterator=driver.find_elements(selector(type),path)
                for data in iterator:
                    temp=''
                    mediaLinks=''
                    t=''    
                    try:
                        type,path=expand_btn
                        if (type!=None) and (path!=None):
                            driver.find_element(selector(type),path).click()
                    except:
                        pass
                    
                    try:
                        type,path = author_name_path
                        author_name= data.find_element(selector(type),path)
                        element_html=author_name.get_attribute('outerHTML')
                        author_name=BeautifulSoup(element_html,'html.parser')
                        author_name=author_name.text
                    except:
                        author_name='not found'    
                    
                    try:        
                        type,path = profile_link_path
                        profile_link= data.find_element(selector(type),path)
                        author_profile_link=profile_link.get_attribute('href')
                    except:
                        author_profile_link='not available'    
                    
                    try:
                        type,path = date_path
                        post_time=data.find_element(selector(type),path)
                        postTime=post_time.get_attribute('data-time')
                        if postTime!=None:
                            t=t+str(postTime)
                    except:
                        postTime='not found'
                    
                    try:
                        if t=='':
                            type,path = date_path
                            post_time=data.find_element(selector(type),path)
                            element_html=post_time.get_attribute('outerHTML')
                            post_time=BeautifulSoup(element_html,'html.parser')
                            post_time=post_time.text
                            try:
                                postTime=str(int(date_coverter(post_time)))
                                if postTime=='None':
                                    postTime=post_time
                            except:
                                postTime=post_time 
                    except:
                        postTime='not found.'
                        
                    try:
                        for b in body_path:
                            type,path = b
                            paras=data.find_elements(selector(type),path)
                            try:
                                for para in paras:
                                    element_html=para.get_attribute('outerHTML')
                                    para=BeautifulSoup(element_html,'html.parser')
                                    try:
                                        para.blockquote.decompose()
                                    except:
                                        pass
                                    temp+=para.text+' '
                            except:
                                pass          
                    except:
                        pass        
                    
                    try:
                        for m in media_path:
                            type,path=m
                            media=data.find_elements(selector(type),path)
                            for i in media:
                                try:
                                    Link=i.get_attribute('href')
                                    mediaLinks+=Link+', ' 
                                except:
                                    pass
                                try:
                                    img_Link=i.get_attribute('src')
                                    if 'gif' not in img_Link:
                                        mediaLinks+=img_Link+', '        
                                except:
                                    pass
                    except:
                        pass

                    post={'author_name':author_name,'author_profile_link':author_profile_link,'date':postTime,'post':temp,'media_links':mediaLinks}
                    allPosts.append(post) 
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
                except:
                    break
            try:   
                firstDate=allPosts[0]['date']
                lastDate=allPosts[-1]['date']
                if round(int(firstDate))<round(int(lastDate)):
                    allPosts.reverse()
            except:
                pass

            if len(allPosts)>0:
                dct={'title':title,'url':threadUrls[p],'posts':allPosts,'lastModifiedDate':lastModDate[p]}
                print(dct)
                collection3.insert_one(dct)
                scrapSuccess(url)
                print(url," Scrapping Done!!")
                # # sendLog(url," Scrapping Done!!")
                isNodeBusy =False
        else:
            print("not Scrapped!!---->",url)
            # sendLog("not Scrapped!!---->",url) #test 3
            print("FailedCount is:",str(int(failedCount)+1))
            # sendLog("FailedCount is:",str(failedCount+1))  #test 2
            scrapFailed(url,int(failedCount)) 
            isNodeBusy =False       