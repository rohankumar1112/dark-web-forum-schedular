from databaseConnection import collection1,collection2
from flag import isNodeBusy
# from flag import sendLog
from scappingForum import forum_scrap
from flag import sendLog,sendData

isNodeBusy = False

def getfunction(data):
        Urls =[]
        Lastmods =[]
        for x in data:
                url=x['url']
                if url not in Urls:
                        Urls.append(url)
                        Lastmods.append(x['lastModDate'])                  
        print(Urls)
        # sendData(Urls)
        try:
                forum_scrap(Urls,Lastmods)
        except:
               pass
                
                
