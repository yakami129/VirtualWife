import logging
import queue
import re
import threading
import traceback
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from ..utils.chat_message_utils import format_chat_text
from ..utils.str_utils import remove_special_characters, remove_emojis
from ..config import singleton_sys_config
from ..emotion.emotion_manage import GenerationEmote
import threading

# 聊天消息通道
chat_channel = "chat_channel"
# 创建一个线程安全的队列
chat_queue = queue.SimpleQueue()
logger = logging.getLogger(__name__)


class RealtimeMessage():
    type: str
    user_name: str
    content: str
    emote: str
    action: str
    expand: str

    def __init__(self, type: str, user_name: str, content: str, emote: str, expand: str = None, action: str = None) -> None:
        self.type = type
        self.user_name = user_name
        self.content = content
        self.emote = emote
        self.action = action
        self.expand = expand

    def to_dict(self):
        return {
            "type": self.type,
            "user_name": self.user_name,
            "content": self.content,
            "emote": self.emote,
            "action": self.action,
            "expand": self.expand
        }


def put_message(message: RealtimeMessage):
    global chat_queue
    chat_queue.put(message)


def send_message():
    global chat_queue
    channel_layer = get_channel_layer()
    send_message_exe = async_to_sync(channel_layer.group_send)

    while True:
        try:
            message = chat_queue.get()
            if (message is not None and message != ''):
                chat_message = {"type": "chat_message",
                                "message":  message.to_dict()}
                send_message_exe(chat_channel, chat_message)
        except Exception as e:
            traceback.print_exc()


def realtime_callback(role_name: str, you_name: str, content: str, end_bool: bool):
    if not hasattr(realtime_callback, "message_buffer"):
        realtime_callback.message_buffer = ""

    realtime_callback.message_buffer += content
    # 如果 content 以结束标点符号或空结尾，打印并清空缓冲区
    if re.match(r"^(.+[。．！？\n]|.{10,}[、,])", realtime_callback.message_buffer) or end_bool:
        realtime_callback.message_buffer = format_chat_text(
            role_name, you_name, realtime_callback.message_buffer)

        # 删除表情符号和一些特定的特殊符号，防止语音合成失败
        message_text = realtime_callback.message_buffer
        message_text = remove_emojis(message_text)
        message_text = remove_special_characters(message_text)

        # 生成人物表情
        generation_emote = GenerationEmote(llm_model_driver=singleton_sys_config.llm_model_driver,
                                           llm_model_driver_type=singleton_sys_config.conversation_llm_model_driver_type)
        emote = generation_emote.generation_emote(
            query=message_text)

        # 发送文本消息
        put_message(RealtimeMessage(
            type="user", user_name=you_name, content=message_text, emote=emote))
        realtime_callback.message_buffer = ""


class RealtimeMessageQueryJobTask():

    @staticmethod
    def start():
        # 创建后台线程
        background_thread = threading.Thread(target=send_message)
        background_thread.daemon = True
        # 启动后台线程
        background_thread.start()
        logger.info("=> Start RealtimeMessageQueryJobTask Success")
