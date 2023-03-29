from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium import webdriver
from datetime import datetime, timedelta
import re
from tbselenium.tbdriver import TorBrowserDriver
from bs4 import BeautifulSoup
import pymongo
from statusHandler import *
import time
import calendar
# import undetected_chromedriver as uc
from Login import login_button_detect,login_fill,detect_login
from driverpath import torPath
from databaseConnection import *
from timestamp_convertor import date_coverter
from startDisplay import *

def addToDb(scraped_doc):
    url = scraped_doc['url']
    db_doc = collection3.find_one({"url": f"{url}"})
    if db_doc :
        id = db_doc['_id']
        db_posts = db_doc['posts']
        
        db_post = db_posts[-1]
        try:
            db_date = date_coverter(f"{db_post['date']}")
        except:
            db_date=db_post['date']
        posts = scraped_doc['posts']
        new_posts = scraped_doc['posts']
        date_failed_count=db_doc['date_failed_count']
        
        new_format=None
        try:
            for post in posts :
                try:
                    
                    post_date = date_coverter(f"{post['date']}")
                    if post_date==None:
                        new_format=post['date']
                        print('new date format detected. New format------->',new_format)  
                    if post_date > db_date:
                        db_posts.append(post)
                except:
                    pass
            q={'_id':id}
            update = {"$set": {"posts": db_posts,'date_failed_count':0}}
            collection3.update_one(q,update)
            print("DataBase Updated!!")
        except:
            q={'_id':id}
            update = {"$set": {"posts": new_posts,'date_failed_count':int(date_failed_count)+1}}
            collection3.update_one(q,update)
            print("DataBase Updated!!")
            # sendLog("DataBase Updated!!")
    else :
        collection3.insert_one(scraped_doc)
        print("Added New Data in DataBase.")
        # sendLog("Adding New Data to DataBase")
        # print("DataBase Updated!!")
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
    if type!=None:
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
        
# functions for dataTime--------------------

def forum_scrap(threadUrls,lastModDate):
    isNodeBusy =True
    title_path=None
    iterator_path =None
    author_name_path =None
    profile_link_path =None
    date_path =None
    body_path =None
    media_path =None
    path_of_next_btn =None
    expand_btn =None
    failedCount =0 

    # xvfb_display = start_xvfb()
    with TorBrowserDriver(torPath) as driver:
        for p in range(min(len(threadUrls),len(lastModDate))):
            url=threadUrls[p]
            failedCount=collection2.find_one({'url':url})['failedCount']  
            domain= url.split('.')[0]
            dataByDomain=collection1.find_one({'site':{'$regex':domain}})
            if dataByDomain==None:
                print('Path not found for this site.')
                # sendLog('Path not found for this site.')
                scrapFailed(url,int(failedCount))
                continue 
            else:
                title_path=dataByDomain['title_path']
                iterator_path =dataByDomain['iterator_path']
                author_name_path =dataByDomain['author_name_path']
                profile_link_path =dataByDomain ['profile_link_path']
                date_path =dataByDomain['date_path']
                body_path =dataByDomain['body_path']
                media_path =dataByDomain['media_path']
                path_of_next_btn =dataByDomain['path_of_next_btn']
                expand_btn =dataByDomain['expand_btn']
                failedCount =dataByDomain['failedCount']

            try:
                print(f"{url} is Scrapping now...")
                # sendLog(f"{url} is Scrapping now...")
            
                scrapRunning(url)
                driver.get(url)
                time.sleep(1)
                try:
                    check=detect_login(driver,url)
                    if check!=True:
                        login_button_detect(driver,url)
                        login_fill(driver)
                    driver.get(url)
                    time.sleep(1)
                except:
                    pass

                
            except:
                scrapFailed(url,int(failedCount)) 
                print(f"Not Scrapped!!----> {url}")
                # sendLog(f"Not Scrapped!!----> {url}")
                print(f"FailedCount is: {str(int(failedCount)+1)}")
                continue
                # sendLog(f"FailedCount is: {str(int(failedCount)+1)}")
    
                # isNodeBusy =False
                
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
                    scrapSuccess(url)
                    dct={'title':title,'url':threadUrls[p],'posts':allPosts,'lastModifiedDate':lastModDate[p],'date_failed_count':0,'scrappedAt':int(datetime.now().timestamp())}
                    print(dct)
                    # sendData(dct)
                    print(url," Scrapping Done!!")
                    # sendLog(f"{url} Scrapping Done!!")
                    addToDb(dct)
                    # isNodeBusy =False
                    
            else:
                scrapFailed(url,int(failedCount)) 
                print("not Scrapped!!---->",url)
                # sendLog(f"not Scrapped!!----> {url}") #test 3
                print("FailedCount is:",str(int(failedCount)+1))
                # sendLog(f"FailedCount is: {str(failedCount+1)}")  #test 2
                # driver.close()
                # isNodeBusy =False 
                continue
    isNodeBusy =False 
    # stop_xvfb(xvfb_display)         