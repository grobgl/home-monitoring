import logging
import schedule
import speedtest
import time
from threading import Thread
from influxdb import InfluxDBClient


_LOGGER = logging.getLogger()


def job():
    _LOGGER.info('Running speedtest ...')
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    res = s.results.dict()

    _LOGGER.info('Speedtest results: download %d, upload %d, ping %d', res['download'], res['upload'], res['ping'])

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


_LOGGER.info('Initialising ...')

global db
db = InfluxDBClient(host='influxdb', port=8086, username='root', password='root', database='speedtest')
db.create_database('speedtest')
db.create_retention_policy('forever', 'INF', 1, default=True)
db.switch_user("dbuser", "dbuser")

schedule.every(5).minutes.do(run_threaded, job)

_LOGGER.info('Initialised')

while 1:
    schedule.run_pending()
    time.sleep(1)

