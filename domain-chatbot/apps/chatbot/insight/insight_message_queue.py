import logging
import queue
import threading
import traceback
from ..utils.chat_message_utils import format_user_chat_text
from ..process import process_core
from ..output import realtime_message_queue

# 创建一个线程安全的队列
insight_message_queue = queue.SimpleQueue()
logger = logging.getLogger(__name__)


class InsightMessage():
    type: str
    user_id: str
    user_name: str
    content: str
    emote: str
    action: str
    expand: str
    is_recite: bool

    def __init__(self, type: str, user_id: str, user_name: str, content: str, emote: str, action: str = None,
                 expand: str = None, is_recite: bool = True) -> None:
        self.type = type
        self.user_id = user_id
        self.user_name = user_name
        self.content = content
        self.emote = emote
        self.action = action
        self.expand = expand
        self.is_recite = is_recite

    def to_dict(self):
        return {
            "type": self.type,
            "user_name": self.user_name,
            "content": self.content,
            "emote": self.emote,
            "action": self.action,
            "expand": self.expand,
            "is_recite": self.is_recite
        }


def put_message(message: InsightMessage):
    global insight_message_queue
    insight_message_queue.put(message)


def send_message():
    while True:
        try:
            message = insight_message_queue.get()
            if (message != None and message != ''):
                if (message.type == "danmaku"):
                    content = format_user_chat_text(text=message.content)
                    realtime_message_queue.put_message(realtime_message_queue.RealtimeMessage(
                        type=message.type,
                        user_name=message.user_name,
                        content=content,
                        emote=message.emote,
                        action=message.action
                    ))
                    process_core.chat(
                        you_name=message.user_name, query=message.content)
        except Exception as e:
            traceback.print_exc()


class InsightMessageQueryJobTask():

    @staticmethod
    def start():
        # 创建后台线程
        background_thread = threading.Thread(target=send_message)
        background_thread.daemon = True

        # 启动后台线程
        background_thread.start()
        logger.info("=> Start InsightMessageQueryJobTask Success")
