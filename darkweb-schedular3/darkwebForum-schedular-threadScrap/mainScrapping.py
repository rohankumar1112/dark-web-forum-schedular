from statusHandler import *
from databaseConnection import *
from flag import isNodeBusy
# from flag import sendLog
from scappingForum import forum_scrap

# Scrapping...
isNodeBusy = False

def getfunction1(data2):
        Urls =[]
        Lastmods =[]
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
        failedCount =None
        for x in data2:
                Urls.append(x['url'])
                Lastmods.append(x['lastModDate'])  
                domain= x['url'].split('.')[0]
                dataByDomain=collection1.find_one({'site':{'$regex':domain}})
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
                forum_scrap(Urls,Lastmods,title_path,iterator_path,author_name_path,profile_link_path,date_path,body_path,media_path,path_of_next_btn,expand_btn,failedCount)
                
                # print(url,"is Scrapping now...")
                # # sendLog(url,"is Scrapping now...")
                # scrapRunning(url)
        
                # # scrapSuccess(url)
                # # print(url," Scrapping Done!!")
                # # # sendLog(url," Scrapping Done!!")
                # # isNodeBusy =False
        except:
               pass
                # print("not Scrapped!!---->",url)
                # # sendLog("not Scrapped!!---->",url) #test 3
                # print("FailedCount is:",str(failedCount+1))
                # # sendLog("FailedCount is:",str(failedCount+1))  #test 2
                # scrapFailed(url,failedCount) 
                # isNodeBusy =False
                
