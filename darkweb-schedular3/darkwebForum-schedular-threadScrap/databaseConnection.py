import pymongo
# MongoDb Connection...
import pymongo
client =pymongo.MongoClient("mongodb+srv://emseccomandcenter:TUXnEN09VNM1drh3@cluster0.psiqanw.mongodb.net/?retryWrites=true&w=majority")

#XPATH fetch collection
db =client['Main_ForumFilter_Data']


collection1 =db['Xpath_forum']
print ("Total websites we have:", collection1.count_documents( {} ))

# link dump collection
collection2 =db['forum_Links']

#Data sump collection
collection3 =db['mainData_test']
login_credential=db['login_credentials']


# domain='https://ezdhgsy2aw7zg54z6dqsutrduhl22moami5zv2zt6urr6vub7gs6wfad'
# dataByDomain=collection1.find_one({'site':{'$regex':domain}})
# print(dataByDomain)