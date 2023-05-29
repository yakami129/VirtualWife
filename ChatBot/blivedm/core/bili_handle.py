import random
import os
import asyncio
from dotenv import load_dotenv
from .handlers import BaseHandler
from .client import BLiveClient
from .models import (HeartbeatMessage,DanmakuMessage,GiftMessage,GuardBuyMessage,SuperChatMessage)
from django.core.management.base import BaseCommand
from django.apps import AppConfig
from .chat_queue_management import put_chat_message
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
        print(f'[{client.room_id}] 当前人气值：{message.popularity}')

    async def _on_danmaku(self, client: BLiveClient, message: DanmakuMessage):
        message_body = {
            "user_name":message.uname,
            "content":message.msg
        }
        put_chat_message(message_body)
        print(f'[{client.room_id}] {message.uname}：{message.msg}')

    async def _on_gift(self, client: BLiveClient, message: GiftMessage):
        print(f'[{client.room_id}] {message.uname} 赠送{message.gift_name}x{message.num}'
              f' （{message.coin_type}瓜子x{message.total_coin}）')

    async def _on_buy_guard(self, client: BLiveClient, message: GuardBuyMessage):
        print(f'[{client.room_id}] {message.username} 购买{message.gift_name}')

    async def _on_super_chat(self, client: BLiveClient, message: SuperChatMessage):
        print(f'[{client.room_id}] 醒目留言 ¥{message.price} {message.uname}：{message.message}')

