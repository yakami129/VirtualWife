import random
import os
import asyncio
from dotenv import load_dotenv
from .handlers import BaseHandler
from .client import BLiveClient
from .models import (HeartbeatMessage,DanmakuMessage,GiftMessage,GuardBuyMessage,SuperChatMessage,LikeInfoV3ClickMessage,EntryEffectMessage,InteractWordMessage)
from django.core.management.base import BaseCommand
from django.apps import AppConfig
from .chat_priority_queue_management import *
import logging
logging.basicConfig(level=logging.INFO)

## 初始化操作
load_dotenv()  # 读取 .env 文件

# 您的应用ID
B_STATION_ID = os.getenv("B_STATION_ID")

# 直播间ID的取值看直播间URL
TEST_ROOM_IDS = [
    B_STATION_ID
]

client = None;
enable = False;

async def start():
    """
    启动监听一个直播间
    """

    global enable
    global client

    if(enable):
        print("[BIZ] biliHandle in progress .....")
        return
    
    print("[BIZ] biliHandle run .....")
    room_id = random.choice(TEST_ROOM_IDS)
    print("room_id:",room_id)
    # 如果SSL验证失败就把ssl设为False，B站真的有过忘续证书的情况
    client = BLiveClient(room_id, ssl=True)
    handler = BiliHandler()
    client.add_handler(handler)
    client.start()
    enable = True
    while(enable):
        await asyncio.sleep(60)

async def stop():
    """
    关闭监听一个直播间
    """

    global enable
    global client

    try:
        enable = False
        await client.join()
    finally:
        await client.stop_and_close()

class BiliHandler(BaseHandler):

    async def _on_heartbeat(self, client: BLiveClient, message: HeartbeatMessage):
        cmd_str  = f'爱莉现在的人气为:{message.popularity}，请使用生动形象开玩笑的方式形容一下你的直播间人气或者讲讲最近发生的一些趣事，语言尽量简短一些，每次都需要使用不同的方式形容'
        message_body = {
            "type":"system",
            "content":'',
            'cmd': cmd_str
        }
        # put_chat_message(message_body)

    async def _on_danmaku(self, client: BLiveClient, message: DanmakuMessage):
        chat_message = message.msg;
        # if chat_message.startswith('#'):
        #     # 如果字符串以 '#' 开头，执行提交游戏答案代码
        #      await sync_to_async(commit_riddle_answer)(user_name=message.uname,riddle_answer=chat_message)
        # elif chat_message.endswith(('?', '。',"？")):
        #     # 如果字符串以 '？'，'。' 结尾，执行闲聊模式
        #     message_str  = f'{chat_message}'
        #     cmd_str  = f'[{message.uname}说]：{chat_message}'
        #     message_body = {
        #         "type":"user",
        #         "user_name":message.uname,
        #         "content":message_str,
        #         'cmd': cmd_str
        #     }
        #     put_chat_message(MessagePriority.CAPTAIN_BARRAGE_MESSAGE,message_body)
        message_str  = f'{chat_message}'
        cmd_str  = f'[{message.uname}说]：{chat_message}'
        message_body = {
            "type":"user",
            "user_name":message.uname,
            "content":message_str,
            'cmd': cmd_str
        }
        put_chat_message(MessagePriority.CAPTAIN_BARRAGE_MESSAGE,message_body)

    async def _on_gift(self, client: BLiveClient, message: GiftMessage):
        cmd_str  = f'{message.uname}赠送{message.gift_name}x{message.num}'
        message_body = {
            "type":"system",
            "content":'',
            'cmd': cmd_str
        }
        put_chat_message(MessagePriority.CAPTAIN_BARRAGE_MESSAGE,message_body)


    async def _on_buy_guard(self, client: BLiveClient, message: GuardBuyMessage):
        cmd_str  = f'{message.username}购买{message.gift_name}'
        message_body = {
            "type":"system",
            "content":'',
            'cmd': cmd_str
        }
        put_chat_message(MessagePriority.SEND_GIFTS_MESSAGE,message_body)

    async def _on_super_chat(self, client: BLiveClient, message: SuperChatMessage):
        print(f'[{client.room_id}] 醒目留言 ¥{message.price} {message.uname}：{message.message}')

    async def _on_like_click(self, client: BLiveClient, message: LikeInfoV3ClickMessage):
        cmd_str  = f'{message.uname}偷偷摸了摸爱莉的头，请开玩笑的方式回绝'
        message_str  = f'{message.uname}偷偷摸了摸爱莉的头'
        message_body = {
            "type":"system",
            "user_name":message.uname,
            "content":message_str,
            'cmd': cmd_str
        }
        put_chat_message(MessagePriority.TOUCH_THE_HEAD_MESSAGE,message_body)

    async def _on_entry_effect(self, client: BLiveClient, message: EntryEffectMessage):
        message_body = {
            "type":"system",
            "content":message.copy_writing
        }
        #put_chat_message(message_body)
        
    async def _on_interact_word(self, client: BLiveClient, message: InteractWordMessage):
        """
        用户进入直播间，用户关注直播间
        """
        message_str  = f'{message.uname}进入了直播间'
        cmd_str  = message_str + '，请简单欢迎，不能超过10个字'
        message_body = {
            "type":"system",
            "content": message_str,
            'cmd': cmd_str
        }
        #put_chat_message(MessagePriority.ENTER_THE_ROOM_MESSAGE,message_body)

