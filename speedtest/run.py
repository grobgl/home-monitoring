import schedule
import speedtest
import time
from threading import Thread
from influxdb import InfluxDBClient


def job():
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    res = s.results.dict()
    res = [ 
              { 
                  'measurement': key,
                  'fields': {
                      'Int_value': res[key] 
                  },
                  'tags': []
              } for key in ['download', 'upload', 'ping'] 
          ]
    db.write_points(res)

def run_threaded(job_func):
    job_thread = Thread(target=job_func)
    job_thread.start()


global db
db = InfluxDBClient(host='influxdb', port=8086, username='root', password='root', database='speedtest')
db.create_database('speedtest')
db.create_retention_policy('forever', 'INF', 1, default=True)
db.switch_user("dbuser", "dbuser")

schedule.every(5).minutes.do(run_threaded, job)

while 1:
    schedule.run_pending()
    time.sleep(1)

