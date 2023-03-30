from databaseConnection import collection1
from mainScrapping import getfunction
from datetime import date, datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from flag import sendLog,sendData
from flag import isNodeBusy
from app import app
import time
from flask import Flask, jsonify, request
# from flask_cors import CORS
# from flask_socketio import SocketIO

def fetchingLinks():
    print(datetime.now())
    # sendLog(datetime.now())
    time.sleep(2)
    if collection1.count_documents({'isUrgent': True}) > 0:
        print(f"No of urgent websites :{collection1.count_documents({'isUrgent':True})}")
        # sendLog(f"No of urgent websites :{collection1.count_documents({'isUrgent':True})}")
        urgent = collection1.find({"isUrgent": True, "status": {"$ne": "running"}}, {})
        getfunction(urgent[0])
    else:
        d = datetime.today() - timedelta(hours=0, minutes=30)
        if collection1.count_documents({"status": {"$ne": "running"}, "time": {"$lte": d}}) > 0:
            print("xx")
            print(f"No of websites whose status not running: {collection1.count_documents({'status':{'$ne':'running'},'time':{'$lte':d}})}")
            # sendLog(f"No of websites whose status not running: {collection1.count_documents({'status':{'$ne':'running'},'time':{'$lte':d}})}")
            urlList = collection1.find(
                {"status": {"$ne": "running"}, "time": {"$lte": d}}, {})
            getfunction(urlList[0])
        else:
            print("Every forums Scrapped!!")
            # sendLog("Every forums Scrapped!!")


fetchingLinks()
@app.route('/')
def hello_world():
    return 'Hello Darkweb-Forum_Threads!!'

sched = BackgroundScheduler(daemon=True)
sched.add_job(fetchingLinks, 'interval', minutes=1)
sched.start()


# main flask function
if __name__ == '__main__':
    # socketio.run(app, debug=True)
    app.run(port =6000,debug=False)
    # sched = BackgroundScheduler(daemon=True)
    # sched.add_job(fetchingLinks, 'interval', minutes=1)
    # sched.start()
    
# Scheduler..
