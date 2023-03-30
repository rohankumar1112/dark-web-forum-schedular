from databaseConnection import collection2
from mainScrapping import getfunction
from datetime import date,datetime,timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from flag import sendLog,sendData
from flag import isNodeBusy
from app import app
import time
# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from flask_socketio import SocketIO

# Flask...

def scrapping():
    print(datetime.now())
    # sendLog(datetime.now())
    if (isNodeBusy!=True):
        time.sleep(5)
        if collection2.count_documents({'isUrgent':True})>0:
                print(f"No of urgent websites :{collection2.count_documents({'isUrgent':True})}")
                # sendLog(f"No of urgent websites :{collection2.count_documents({'isUrgent':True})}")
                urgent=collection2.find({"isUrgent":True,"status":{"$ne":"running"}},{})
                time.sleep(1)
                getfunction(urgent)     
        else:
            d = datetime.today() - timedelta(hours=0, minutes=5)
            if collection2.count_documents({"status":{"$ne":"running"},"time":{"$lte":d}})>0:
                print(f"No of websites whose status not running: {collection2.count_documents({'status':{'$ne':'running'},'time':{'$lte':d}})}")
                # sendLog(f"No of websites whose status not running: {collection2.count_documents({'status':{'$ne':'running'},'time':{'$lte':d}})}")
                urlList =collection2.find({"status":{"$ne":"running"},"time":{"$lte":d}},{})
                getfunction(urlList)    
            else:
                print("Every url Scrapped!!")   
                # sendLog("Every url Scrapped!!")   
    else:
        print("Node is Busy!!")        
        # sendLog("Node is Busy!!")        

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