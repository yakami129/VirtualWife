import asyncio
import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Callable

from bilibili_api import live, sync, Credential
import http.cookies

from bilibili_api.live import LiveDanmaku

logger = logging.getLogger(__name__)


class BilibiliLiveListener:
    credential: Credential
    live_danmaku: LiveDanmaku
    character_name: str

    def __init__(self, room_id: str, credential: Credential, character_name: str):
        from ..insight_message_queue import InsightMessage, put_message
        self.credential = credential
        self.character_name = character_name
        room = live.LiveDanmaku(room_display_id=room_id, credential=credential, max_retry=3)

        @room.on('DANMU_MSG')
        async def on_danmaku(event):
            # 收到弹幕
            data_info = event["data"]["info"]
            user_id = data_info[0][15]["user"]["uid"]
            user_name = data_info[0][15]["user"]["base"]["name"]
            content = data_info[1]
            logging.info(f"收到弹幕 user_id:{user_id} user_name：{user_name} content:{content}")
            put_message(InsightMessage(
                type="danmaku", user_id=user_id, user_name=user_name, content=content, emote="neutral",
                action=""))

        @room.on('SEND_GIFT')
        async def on_gift(event):
            data_info = event["data"]
            # 收到礼物
            logging.info("收到礼物：" + json.dumps(data_info, ensure_ascii=False))

        @room.on('INTERACT_WORD')
        async def on_interact_word(event):
            # 用户进入直播间
            data_info = event["data"]["data"]
            user_name = data_info["uname"]
            user_id = data_info["uid"]
            logging.info(f"{user_name}进入直播间")
            put_message(InsightMessage(
                type="danmaku", user_id=user_id, user_name=user_name, content=f"欢迎{user_name}进入直播间",
                emote="relaxed",
                action="standing_greeting"))

        @room.on('ROOM_REAL_TIME_MESSAGE_UPDATE')
        async def on_room_real_time_message_update(event):
            # 粉丝数更新
            logging.info("粉丝数更新:" + json.dumps(event, ensure_ascii=False))

        @room.on('LIKE_INFO_V3_CLICK')
        async def on_like_click(event):
            data_info = event["data"]["data"]
            user_name = data_info["uname"]
            user_id = data_info["uid"]
            message_str = f'{user_name}偷偷摸了摸{self.character_name}的头'
            put_message(InsightMessage(
                type="danmaku", user_id=user_id, user_name=user_name, content=message_str, emote="relaxed",
                action="excited"))

        self.live_danmaku = room

    async def open(self):
        await self.live_danmaku.connect()

    async def close(self):
        await self.live_danmaku.disconnect()


class ThreadPoolManager:
    def __init__(self, max_workers: int):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def run_in_thread(self, func: Callable, *args, **kwargs):
        """
        在线程池中运行一个函数。
        :param func: 要运行的函数。
        :param args: 函数的位置参数。
        :param kwargs: 函数的关键字参数。
        :return: Future对象，代表异步执行的操作。
        """
        return self.executor.submit(func, *args, **kwargs)

    def shutdown(self):
        """
        清理线程池，等待线程池中的任务完成后关闭。
        """
        self.executor.shutdown(wait=True)


def start(listener: BilibiliLiveListener):
    # 创建一个新的事件循环
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # 创建并运行 BilibiliLiveListener
    loop.run_until_complete(listener.open())


def lazy_bilibili_live(sys_config_json: any, sys_cofnig: any):
    if sys_cofnig.bilibili_live_listener is not None:
        try:
            asyncio.run(sys_cofnig.bilibili_live_listener.close())
            sys_cofnig.thread_pool_manager.shutdown()
        except Exception as e:
            logger.warning(e)
        logger.info(f" 终止B站弹幕监听程序")

    enableLive = sys_config_json["enableLive"]
    if enableLive:
        room_id = str(sys_config_json["liveStreamingConfig"]["B_ROOM_ID"])
        cookie_text = str(sys_config_json["liveStreamingConfig"]["B_COOKIE"])
        cookie = http.cookies.SimpleCookie()
        cookie.load(cookie_text)

        sessdata = cookie.get("SESSDATA").value
        bili_jct = cookie.get("bili_jct").value
        dedeuserid = cookie.get("DedeUserID").value
        credential = Credential(sessdata=sessdata, bili_jct=bili_jct, buvid3="", dedeuserid=dedeuserid)
        sys_cofnig.bilibili_live_listener = bilibili_live_listener = BilibiliLiveListener(room_id=room_id,
                                                                                          credential=credential,
                                                                                          character_name=
                                                                                          sys_config_json[
                                                                                              "characterConfig"][
                                                                                              "character_name"])
        sys_cofnig.thread_pool_manager = thread_pool_manager = ThreadPoolManager(max_workers=1)
        thread_pool_manager.run_in_thread(start, bilibili_live_listener)
        logger.info(f"开启B站直播 room_id:{room_id}")


if __name__ == '__main__':
    # 创建一个 Cookie 对象
    cookie_text = "LIVE_BUVID=AUTO2816977204552676; b_nut=1697720455; buvid4=34DB59A6-47D1-B3DC-953E-0E39DB1D2E1655624-023101921-ksPq5hUPXVm6%2BOFFmBjPRg%3D%3D; buvid3=37A48A8B-FF98-401C-B2BE-AC57D04DC1EC27577infoc; _uuid=D10C5239E-95510-3EDF-2A8E-F134F5686EB1069650infoc; buvid_fp_plain=undefined; enable_web_push=DISABLE; header_theme_version=CLOSE; CURRENT_FNVAL=4048; rpdid=|(kJYkJkJ)m|0J'uYm~~mJuYR; DedeUserID=382957163; DedeUserID__ckMd5=537234e3cc45dfda; hit-dyn-v2=1; CURRENT_QUALITY=80; bp_article_offset_382957163=874973829923864664; fingerprint=dff334dfe228c7ed3101952831bcec25; buvid_fp=dff334dfe228c7ed3101952831bcec25; home_feed_column=5; PVID=1; SESSDATA=ebbe501f%2C1720139869%2Ce6249%2A12CjCJU4P7mak9oluUq8CXdXfVZFz-ZPeAica88Ng6LC8xjvHy2BB3Z4m0uXcc_GMY-8ISVncwQndJd3liN3l1dFFVSEo1YndtNGNKUmlfZVN0WEJOOGdyYWQ5LTh6cVotb1ItZGVfWExiV1NVcWdlU3dFczMyRWRhZkF2QV9vQ2pFRzVFeXdvX3dBIIEC; bili_jct=fa9c0262144f89b0bc299c5769defb89; b_lsid=585F22B2_18CE16AA261; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDQ4NTA3NjgsImlhdCI6MTcwNDU5MTUwOCwicGx0IjotMX0.csRZa7_FgulmbJFlkc1OWUPpEvQc7rHu79w2mEv0JNo; bili_ticket_expires=1704850708; sid=6gnena0l; bp_video_offset_382957163=883705876426260483; browser_resolution=1440-779; innersign=0"
    cookie = http.cookies.SimpleCookie()
    cookie.load(cookie_text)

    sessdata = cookie.get("SESSDATA")
    bili_jct = cookie.get("bili_jct")
    sessdata_value = sessdata.value
    bili_jct_value = bili_jct.value
    credential = Credential(sessdata=sessdata_value, bili_jct=bili_jct_value, buvid3="")
    bilibili_live_listener = BilibiliLiveListener(room_id=27568443, credential=credential)

    # 创建线程池管理器实例
    thread_pool_manager = ThreadPoolManager(max_workers=1)

    # 将任务提交到线程池
    future = thread_pool_manager.run_in_thread(start, bilibili_live_listener)
    print("start")

    while True:
        time.sleep(10)

    asyncio.run(bilibili_live_listener.close())
    print("stop")
    thread_pool_manager.shutdown()
