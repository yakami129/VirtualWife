import queue
import threading
import asyncio
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# 聊天消息通道
chat_channel = "chat_channel"

# 创建一个线程安全的队列
chat_queue = queue.Queue()


def put_chat_message(chat_message):
    global chat_queue
    chat_queue.put(chat_message)
     
def start_chat_queue_handle():
   
    # 创建后台线程
    background_thread = threading.Thread(target=send_message)
    # 将后台线程设置为守护线程，以便在主线程结束时自动退出
    background_thread.daemon = True
    # 启动后台线程
    background_thread.start()

def send_message():
    global chat_queue
    channel_layer = get_channel_layer()
    send_message_exe = async_to_sync(channel_layer.group_send)
    while True:
        message = chat_queue.get();
        if(message != None):
            chat_message = {"type":"chat_message","message":message}
            print("[BIZ] send_chat_message:",chat_message)
            send_message_exe(chat_channel,chat_message)
  