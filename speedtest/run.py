import schedule
import speedtest
import time
from influxdb import InfluxDBClient


def job():
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    res = s.results.dict()
    res = { key: res[key] for key in ['download', 'upload', 'ping'] }
    db.write(res)

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


global db
db = InfluxDBClient(host='influxdb', port=8086, username='root', password='root', database='speedtest')

# db.create_retention_policy('forever', 'INF', 1)

schedule.every(5).minutes.do(run_threaded, job)

while 1:
    schedule.run_pending()
    time.sleep(1)

