from statusHandler import scrapRunning,scrapFailed,scrapSuccess
from databaseConnection import *
from flag import isNodeBusy
from flag import sendLog
from GetThreadLinks import getThreadLinks

# Scrapping...
isNodeBusy = False


def getfunction(data):
        print("Scrapping in progress...")
        # sendLog("Scrapping in progress...")
        isNodeBusy =True
        site =data['site']
        sectionPath =data['sectionPath']
        urlPath =data['urlPath']
        lastModPath =data['lastModPath']
        path_of_sectionNext_btn =data['path_of_sectionNext_btn']
        failedCount =data['failedCount']
        
        try:              
                print(site,"is Scrapping now...")
                # sendLog(site,"is Scrapping now...")
                scrapRunning(site)
                check=getThreadLinks(site,sectionPath,urlPath,lastModPath,path_of_sectionNext_btn)
                if check==False:
                        print("not Scrapped!!---->",site)
                        # sendLog("not Scrapped!!---->",site) #test 3
                        print("FailedCount is:",str(failedCount+1))
                        # sendLog("FailedCount is:",str(failedCount+1))  
                        scrapFailed(site,failedCount) 
                        isNodeBusy =False
                else:
                        scrapSuccess(site)
                        print(site," Scrapping Done!!")
                        # sendLog(site," Scrapping Done!!")
                        isNodeBusy =False
        except:
                print("not Scrapped!!---->",site)
                # sendLog("not Scrapped!!----> {site}") 
                print("FailedCount is:",str(failedCount+1))
                # sendLog("FailedCount is: {str(failedCount+1)}")  
                scrapFailed(site,failedCount) 
                isNodeBusy =False
                
