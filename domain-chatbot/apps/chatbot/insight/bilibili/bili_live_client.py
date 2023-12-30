import asyncio
import os
import threading

from dotenv import load_dotenv
from .sdk.handlers import BaseHandler
from .sdk.client import BLiveClient
from .sdk.models import (EntryEffectMessage, HeartbeatMessage, DanmakuMessage, GiftMessage, GuardBuyMessage,
                         SuperChatMessage, LikeInfoV3ClickMessage, InteractWordMessage)
from ..insight_message_queue import InsightMessage, put_message
import logging
logger = logging.getLogger(__name__)

load_dotenv()


class BiliLiveClient():

    client: BLiveClient
    room_id: str
    uid: int = 0
    cookie_str: str

    def __init__(self) -> None:
        logger.debug(
            "====================== init BLiveClient ====================== ")
        self.room_id = os.environ['B_STATION_ID']
        uid = os.environ['B_UID']
        if uid:
            self.uid = int(uid)
        self.cookie_str = os.environ['B_COOKIE']
        logger.debug(f"=> room_id:{ self.room_id}")
        logger.debug(f"=> uid:{self.uid}")
        logger.debug(f"=> cookie_str:{self.cookie_str}")
        logger.info("=> Init BLiveClient Success")

    async def start(self):
        self.client = BLiveClient(
            room_id=self.room_id, uid=self.uid, ssl=True, cookie_str=self.cookie_str)
        handler = BiliHandler(room_id=self.room_id)
        self.client.add_handler(handler)
        self.client.start()
        logger.info("=> Start BLiveClient Success")
        enable = True
        while (enable):
            await asyncio.sleep(60)

    async def stop(self):
        self.client.join()
        self.client.stop_and_close()
        logger.info("=> Stop BLiveClient Success")


class BiliHandler(BaseHandler):

    room_id: str

    def __init__(self, room_id: str) -> None:
        super().__init__()
        self.room_id = room_id

    async def _on_heartbeat(self, client: BLiveClient, message: HeartbeatMessage):
        cmd_str = f'爱莉现在的人气为:{message.popularity}，请使用生动形象开玩笑的方式形容一下你的直播间人气或者讲讲最近发生的一些趣事，语言尽量简短一些，每次都需要使用不同的方式形容'
        message_body = {
            "type": "system",
            "content": '',
            'cmd': cmd_str
        }

    async def _on_danmaku(self, client: BLiveClient, message: DanmakuMessage):
        put_message(InsightMessage(
            type="danmaku", user_name=message.uname, content=message.msg, emote="neutral", action=""))

    async def _on_gift(self, client: BLiveClient, message: GiftMessage):
        message_str = f'{message.uname}赠送{message.gift_name}x{message.num}'
        put_message(InsightMessage(
            type="danmaku", user_name=message.uname, content=message_str, emote="happy", action=""))

    async def _on_buy_guard(self, client: BLiveClient, message: GuardBuyMessage):
        message_str = f'{message.username}购买{message.gift_name}'
        put_message(InsightMessage(
            type="danmaku", user_name=message.gift_name, content=message_str, emote="happy", action=""))

    async def _on_super_chat(self, client: BLiveClient, message: SuperChatMessage):
        logger.debug(
            f'[{client.room_id}] 醒目留言 ¥{message.price} {message.uname}：{message.message}')

    async def _on_like_click(self, client: BLiveClient, message: LikeInfoV3ClickMessage):
        message_str = f'{message.uname}偷偷摸了摸爱莉的头'
        put_message(InsightMessage(
            type="danmaku", user_name=message.uname, content=message_str, emote="happy", action="excited"))

    async def _on_interact_word(self, client: BLiveClient, message: InteractWordMessage):
        """
        用户进入直播间，用户关注直播间
        """
        message_str = f'{message.uname}进入了直播间，欢迎欢迎'
        put_message(InsightMessage(
            type="danmaku", user_name=user_name, content=message_str, emote="happy", action="standing_greeting"))
        
    async def _on_entry_effect(self, client: BLiveClient, message: EntryEffectMessage):
        """
        用户进入直播间
        """
        message_str = message.copy_writing
        message_str = message_str.replace("<%","")
        message_str = message_str.replace("%>","")
        put_message(InsightMessage(
            type="danmaku", user_name="system", content=message_str, emote="happy", action="standing_greeting"))

enable_bili_live = False


def bili_live_client_main():
    global enable_bili_live
    if enable_bili_live == False:
        background_thread = threading.Thread(target=start_bili_live_client)
        # 将后台线程设置为守护线程，以便在主线程结束时自动退出
        background_thread.daemon = True
        # 启动后台线程
        background_thread.start()
        enable_bili_live = True
        logger.info("=> Start BiliLiveClient Success")


def start_bili_live_client():
    client = BiliLiveClient()
    asyncio.run(client.start())
