import queue
import threading
import asyncio
import json
import logging
import time
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# 聊天消息通道
chat_channel = "chat_channel"

'''消息优先级'''

class MessagePriority:
    # 游戏回复消息
    GAME_ERPLY_MESSAGE = 1
    # 游戏消息
    GAME_MESSAGE = 2
    # 舰长弹幕消息
    CAPTAIN_BARRAGE_MESSAGE = 3
    # 活跃用户消息
    ACTIVE_USER_BARRAGE_MESSAGE = 4
    # 触摸头消息
    TOUCH_THE_HEAD_MESSAGE = 5
    # 进入房间消息
    ENTER_THE_ROOM_MESSAGE = 6
    # 送礼物消息
    SEND_GIFTS_MESSAGE = 7
    # 默认消息
    DEFAULT_MESSAGE = 10

# 创建一个线程安全的优先级队列
chat_queue =queue.PriorityQueue()

def put_chat_message(priority: int,chat_message: dict[str,str]):
    global chat_queue
    chat_queue.put((priority,chat_message))
     
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
        if(message != None and message != ''):
            chat_message = {"type":"chat_message","message":message[1],"priority":message[0]}
            send_message_exe(chat_channel,chat_message)
  