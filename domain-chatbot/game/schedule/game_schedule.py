import time
import logging
import threading
from ..service.game_service import riddle_queue
from blivedm.core.chat_priority_queue_management import put_chat_message,MessagePriority

def job():

    if riddle_queue.empty()==False:
        
        qsize = riddle_queue.qsize();
        riddle_message = riddle_queue.queue[qsize-1]
        if riddle_message != None and riddle_message != '':

            current_riddle_answer = riddle_message['current_riddle_answer']
            current_riddle_type = riddle_message['current_riddle_type']
            current_riddle_count = riddle_message['current_riddle_count']
            current_riddle_description = riddle_message['current_riddle_description']

            cmd_str  = f'现在粉丝都猜不出答案，需要你给出一些提示，谜题答案：{current_riddle_answer}，谜题的类型是：{current_riddle_type}，当前谜题答案字数是：{current_riddle_count}，谜题描述：{current_riddle_description},请适当透露一些信息给粉丝，一定不能直接透露答案和出现答案的字眼，请模糊透露。'
            message_body = {
                "type":"system",
                "content":'',
                'cmd': cmd_str
            }
            put_chat_message(MessagePriority.GAME_MESSAGE,message_body)


def run_job_every_interval(interval, job):
    threading.Timer(interval, run_job_every_interval, [interval, job]).start()
    job()
    logging.info("[BIZ] 启动谜题提示定时任务")

# 运行 job 函数，每 50 秒运行一次
run_job_every_interval(50, job)