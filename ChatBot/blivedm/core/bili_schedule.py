import time
import threading
from .chat_priority_queue_management import put_chat_message

def job():
     cmd_str  = '爱莉现在的人气比较低'
     message_body = {
        "type":"system",
        "content":'',
        'cmd': cmd_str
     }
     put_chat_message(10,message_body)


def run_job_every_interval(interval, job):
    threading.Timer(interval, run_job_every_interval, [interval, job]).start()
    job()

# 运行 job 函数，每 300 秒运行一次
run_job_every_interval(300, job)