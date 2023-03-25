from databaseConnection import collection1,collection2
from flag import isNodeBusy
# from flag import sendLog
from scappingForum import forum_scrap

isNodeBusy = False

def getfunction(data):
        Urls =[]
        Lastmods =[]
        for x in data:
                Urls.append(x['url'])
                Lastmods.append(x['lastModDate'])                  
        print(Urls)
        try:
                forum_scrap(Urls,Lastmods)
        except:
               pass
                
                
