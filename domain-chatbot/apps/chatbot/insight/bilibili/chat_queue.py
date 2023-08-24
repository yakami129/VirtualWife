import queue
import threading
import traceback
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import threading

# 聊天消息通道
chat_channel = "chat_channel"
# 创建一个线程安全的优先级队列
chat_queue = queue.SimpleQueue()


class ChatMessage():
    type: str
    user_name: str
    content: str
    expand: str
    priority: int

    def __init__(self, type: str, user_name: str, content: str, expand: str = None, priority: int = 10) -> None:
        self.type = type
        self.user_name = user_name
        self.content = content
        self.expand = expand
        self.priority = priority

    def to_dict(self):
        return {
            "type": self.type,
            "user_name": self.user_name,
            "content": self.content,
            "priority": self.priority,
            "expand": self.expand
        }


class MessagePriority:
    '''消息优先级'''
    # 最高优先级弹幕消息
    HIGHEST_BARRAGE_MESSAGE = 1
    # 触摸头消息
    TOUCH_THE_HEAD_MESSAGE = 2
    # 送礼物消息
    SEND_GIFTS_MESSAGE = 3
    # 用户弹幕消息
    USER_MESSAGE = 4
    # 进入房间消息
    ENTER_THE_ROOM_MESSAGE = 5
    # 默认消息
    DEFAULT_MESSAGE = 10


def put_chat_message(message: ChatMessage):
    global chat_queue
    chat_queue.put(message)


def send_message():
    global chat_queue
    try:
        channel_layer = get_channel_layer()
        send_message_exe = async_to_sync(channel_layer.group_send)
        while True:
            message = chat_queue.get()
            if (message != None and message != ''):
                chat_message = {"type": "chat_message",
                                "message":  message.to_dict(), "priority": message.priority}
                send_message_exe(chat_channel, chat_message)
    except Exception as e:
        traceback.print_exc()


class QueryJobTask():

    @staticmethod
    def start():
        # 创建后台线程
        background_thread = threading.Thread(target=send_message)
        # 将后台线程设置为守护线程，以便在主线程结束时自动退出
        background_thread.daemon = True
        # 启动后台线程
        background_thread.start()
        print("=> QueryJobTask start")
