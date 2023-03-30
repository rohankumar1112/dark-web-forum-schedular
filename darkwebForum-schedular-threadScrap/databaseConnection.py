import pymongo
from flag import sendLog,sendData
client =pymongo.MongoClient("mongodb+srv://emseccomandcenter:TUXnEN09VNM1drh3@cluster0.psiqanw.mongodb.net/?retryWrites=true&w=majority")

#XPATH fetch collection
db =client['Main_ForumFilter_Data']
collection1 =db['Xpath_forum']

# link dump collection
collection2 =db['forum_Links']
print(f"Total Links we have: {collection2.count_documents( {} )}")
# sendLog(f"Total Links we have:{collection2.count_documents( {} )}")

#Data Dump collection
collection3 =db['mainForum_Data']
login_credential=db['login_credentials']


# domain='https://ezdhgsy2aw7zg54z6dqsutrduhl22moami5zv2zt6urr6vub7gs6wfad'
# dataByDomain=collection1.find_one({'site':{'$regex':domain}})
# print(dataByDomain)