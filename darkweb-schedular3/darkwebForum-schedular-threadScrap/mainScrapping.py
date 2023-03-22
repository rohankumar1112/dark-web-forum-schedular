from databaseConnection import collection1,collection2
from flag import isNodeBusy
# from flag import sendLog
from scappingForum import forum_scrap

isNodeBusy = False

def getfunction(data):
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
        for x in data:
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
        except:
               pass
                
                
