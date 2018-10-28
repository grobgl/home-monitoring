import logging
import os

import schedule
import speedtest
import time
from threading import Thread
from influxdb import InfluxDBClient


_LOG_LEVEL = os.environ.get('LOG_LEVEL')
logging.basicConfig(level=_LOG_LEVEL if _LOG_LEVEL else 'WARNING')
_LOGGER = logging.getLogger(__name__)

_INFLUX_DB_USER = os.environ.get('INFLUXDB_USER')
_INFLUX_DB_PASSWORD = os.environ.get('INFLUXDB_USER_PASSWORD')

_SCHEDULE_INTERVAL_MINS = int(os.environ.get('INTERVAL_MINS'))


def job():
    _LOGGER.info('Running speedtest ...')
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    res = s.results.dict()

    _LOGGER.info(
        'Speedtest results: download %d, upload %d, ping %d',
        res['download'],
        res['upload'],
        res['ping'])

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
db = InfluxDBClient(
    host='influxdb',
    port=8086,
    username=_INFLUX_DB_USER,
    password=_INFLUX_DB_PASSWORD,
    database='speedtest')
db.create_database('speedtest')
db.create_retention_policy('forever', 'INF', 1, default=True)
db.switch_user("dbuser", "dbuser")
_LOGGER.info('Initialised')

job()  # run immediately
schedule.every(_SCHEDULE_INTERVAL_MINS).minutes.do(run_threaded, job)

while 1:
    schedule.run_pending()
    time.sleep(1)

