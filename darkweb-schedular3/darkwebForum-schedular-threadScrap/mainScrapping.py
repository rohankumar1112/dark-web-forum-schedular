from statusHandler import *
from databaseConnection import *
from flag import isNodeBusy
# from flag import sendLog
from scappingForum import forum_scrap

# Scrapping...
isNodeBusy = False

def getfunction1(data):
        print("Scrapping in progress...")
        # sendLog("Scrapping in progress...")
        isNodeBusy =True
        url =data['site']
        lastmod,title_path =data['lastmod,title_path']
        iterator_path =data['iterator_path']
        author_name_path =data['author_name_path']
        profile_link_path =data ['profile_link_path']
        date_path =data['date_path']
        body_path =data['body_path']
        media_path =data['media_path']
        path_of_next_btn =data['path_of_next_btn']
        expand_btn =data['expand_btn']
        failedCount =data['failedCount']
        
        try:              
                print(url,"is Scrapping now...")
                # sendLog(url,"is Scrapping now...")
                scrapRunning(url)
                forum_scrap(url,lastmod,title_path,iterator_path,author_name_path,profile_link_path,date_path,body_path,media_path,path_of_next_btn,expand_btn)
                scrapSuccess(url)
                print(url," Scrapping Done!!")
                # sendLog(url," Scrapping Done!!")
                isNodeBusy =False
        except:
                print("not Scrapped!!---->",url)
                # sendLog("not Scrapped!!---->",url) #test 3
                print("FailedCount is:",str(failedCount+1))
                # sendLog("FailedCount is:",str(failedCount+1))  #test 2
                scrapFailed(url,failedCount) 
                isNodeBusy =False
                
