
import logging
import queue
import threading
import traceback
from ..config import singleton_sys_config

logger = logging.getLogger(__name__)

# 创建一个线程安全的优先级队列
chat_history_queue = queue.SimpleQueue()


class ChatHistoryMessage():
    '''定义聊天历史消息队列'''
    role_name: str
    role_message: str
    you_name: str
    you_message: str

    def __init__(self, role_name: str, role_message: str, you_name: str, you_message: str) -> None:
        self.role_name = role_name
        self.role_message = role_message
        self.you_name = you_name
        self.you_message = you_message

    def to_dict(self):
        return {
            "role_name": self.role_name,
            "role_message": self.role_message,
            "you_name": self.you_name,
            "you_message": self.you_message
        }


def put_message(message: ChatHistoryMessage):
    global chat_history_queue
    chat_history_queue.put(message)


def send_message():
    global chat_history_queue
    while True:
        try:
            message = chat_history_queue.get()
            if (message != None and message != ''):
                singleton_sys_config.memory_storage_driver.save(
                    message.you_name, message.you_message, message.role_name, message.role_message)
        except Exception as e:
            traceback.print_exc()


def conversation_end_callback(role_name: str,  role_message: str, you_name: str, you_message: str):
    put_message(ChatHistoryMessage(
        role_name=role_name,
        role_message=role_message,
        you_name=you_name,
        you_message=you_message
    ))


class ChatHistoryMessageQueryJobTask():
    @staticmethod
    def start():
        # 创建后台线程
        background_thread = threading.Thread(target=send_message)
        # 将后台线程设置为守护线程，以便在主线程结束时自动退出
        background_thread.daemon = True
        # 启动后台线程
        background_thread.start()
        logger.info("=> Start ChatHistoryMessageQueryJobTask Success")
