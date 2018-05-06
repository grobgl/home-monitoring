import schedule
import speedtest
import time

def job():
    print("Start speedtest")
    s = speedtest.Speedtest()
    print("get best server")
    s.get_best_server()
    print("download")
    s.download()
    print("upload")
    s.upload()
    print(s.results.dict())

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

job()
# schedule.every(5).minutes.do(run_threaded, job)

# while 1:
#     schedule.run_pending()
#     time.sleep(1)

