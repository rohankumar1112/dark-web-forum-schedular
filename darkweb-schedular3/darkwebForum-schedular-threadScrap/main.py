from databaseConnection import collection1,collection2
from mainScrapping import getfunction1
from datetime import date,datetime,timedelta
from apscheduler.schedulers.background import BackgroundScheduler
# from flag import sendLog,sendData
from flag import isNodeBusy
from app import app
import time
# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from flask_socketio import SocketIO

# Flask...

def scrapping():
    print(datetime.now())
    if (isNodeBusy!=True):
        time.sleep(5)
        if collection2.count_documents({'isUrgent':True})>0:
                print(f"No of urgent websites :{collection2.count_documents({'isUrgent':True})}")
                urgent=collection2.find({"isUrgent":True,"status":{"$ne":"running"}},{})
                getfunction1(urgent) 
     
        else:
            d = datetime.today() - timedelta(hours=0, minutes=30)
            if collection2.count_documents({"status":{"$ne":"running"},"time":{"$lte":d}})>0:
                print(f"No of websites whose status not running: {collection2.count_documents({'status':{'$ne':'running'},'time':{'$lte':d}})}")
                urlList =collection2.find({"status":{"$ne":"running"},"time":{"$lte":d}},{})
                getfunction1(urlList)    
            else:
                print("Every url Scrapped!!") 
                
    else:
        print("Node is Busy!!")        
        
@app.route('/')
def hello_world():
	return 'Hello Darkweb!!'  

scrapping()

# main flask function
if __name__ == '__main__':
    # socketio.run(app, debug=True)
    app.run(debug=True)


# Scheduler..
sched = BackgroundScheduler(daemon=True)
sched.add_job(scrapping,'interval',minutes=1)
sched.start()