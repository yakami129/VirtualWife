
import asyncio
import logging
from .bili_handle import start,stop
from .chat_priority_queue_management import start_chat_queue_handle
import threading

def start_handle():

    # 创建后台线程
    background_thread = threading.Thread(target=run_start)
    # 将后台线程设置为守护线程，以便在主线程结束时自动退出
    background_thread.daemon = True
    # 启动后台线程
    background_thread.start()
    logging.debug("[BIZ] start blivedm_handel....")

    start_chat_queue_handle();
    logging.debug("[BIZ] chat_queue_handle")
       

def run_start():
    # 在新的事件循环中运行异步函数
    asyncio.run(start())

async def stop_handle():
    await stop()
