import schedule
import speedtest
import time

def job():
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    print(s.results.dict())

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

schedule.every(5).minutes.do(run_threaded, job)

while 1:
    schedule.run_pending()
    time.sleep(1)

