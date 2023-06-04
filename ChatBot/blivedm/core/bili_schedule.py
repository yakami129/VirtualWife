import time
import threading
from .chat_queue_management import put_chat_message

def job():
     cmd_str  = '爱莉现在的人气比较低，你需要想办法活跃一下直播间气氛，可以讲故事、提供聊天话题或者生动形象开玩笑的方式形容直播间的状况，语言尽量简短一些，每次都需要使用不同的文案表达'
     message_body = {
        "type":"system",
        "content":'',
        'cmd': cmd_str
     }
     put_chat_message(message_body)


def run_job_every_interval(interval, job):
    threading.Timer(interval, run_job_every_interval, [interval, job]).start()
    job()

# 运行 job 函数，每 300 秒运行一次
#run_job_every_interval(300, job)