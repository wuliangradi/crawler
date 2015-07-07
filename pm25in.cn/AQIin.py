#coding=utf-8
# 爬取pm25in网站上的数据
"""
---- author = "liang wu" ----
---- time = "20150405" ----
---- Email = "wl062345@gmail.com" ----
"""
from datetime import datetime
from apscheduler.scheduler import Scheduler
import time
import json
import csv

import logging
logging.basicConfig()

import sys
reload(sys)
sys.setdefaultencoding('utf8')

def getJson():
    token = "************"
    import requests as r
    result = r.get("http://www.pm25.in/api/querys/all_cities.json",params={"token":token})
    print result
    return result.json()

def saveData():
    print "saveing!"
    data = getJson()

    date = datetime.now().date()
    dateStr = str(date)
    hour = datetime.now().hour
    hourStr = str(hour)
    nameStr = dateStr+'-'+hourStr

    file(nameStr+'.json','w').write(json.dumps(data,indent=2))
    f = open(nameStr+'.json')
    jsoned = json.load(f)
    f.close()
    with open(nameStr+'.csv','wb+') as csv_file:
        csv_writer = csv.writer(csv_file)
        for item in jsoned:
            csv_writer.writerow([item[u'pm2_5'],item[u'primary_pollutant'],item[u'co'],item[u'pm10'],item[u'area'],item[u'o3_8h'],
                       item[u'o3'],item[u'o3_24h'],item[u'station_code'],item[u'quality'],item[u'co_24h'],item[u'no2_24h'],
                       item[u'so2'],item[u'so2_24h'],item[u'time_point'],item[u'pm2_5_24h'],item[u'position_name'],
                       item[u'o3_8h_24h'],item[u'aqi'],item[u'pm10_24h'],item[u'no2']])

if __name__ == '__main__':
    saveData()

    scheduler = Scheduler()
    scheduler.daemonic = False
    scheduler.add_interval_job(saveData,seconds=3600)

    print('One Hour')
    scheduler.start()
