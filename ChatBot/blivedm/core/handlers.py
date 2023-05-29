# -*- coding: utf-8 -*-
import logging
from typing import *

from . import client as client_
from . import models

__all__ = (
    'HandlerInterface',
    'BaseHandler',
)

logger = logging.getLogger('blivedm')

IGNORED_CMDS = (
    'COMBO_SEND',
    'ENTRY_EFFECT',
    'HOT_RANK_CHANGED',
    'HOT_RANK_CHANGED_V2',
    'INTERACT_WORD',
    'LIVE',
    'LIVE_INTERACTIVE_GAME',
    'NOTICE_MSG',
    'ONLINE_RANK_COUNT',
    'ONLINE_RANK_TOP3',
    'ONLINE_RANK_V2',
    'PK_BATTLE_END',
    'PK_BATTLE_FINAL_PROCESS',
    'PK_BATTLE_PROCESS',
    'PK_BATTLE_PROCESS_NEW',
    'PK_BATTLE_SETTLE',
    'PK_BATTLE_SETTLE_USER',
    'PK_BATTLE_SETTLE_V2',
    'PREPARING',
    'ROOM_REAL_TIME_MESSAGE_UPDATE',
    'STOP_LIVE_ROOM_LIST',
    'SUPER_CHAT_MESSAGE_JPN',
    'WIDGET_BANNER',
)
"""常见可忽略的cmd"""

logged_unknown_cmds = set()
"""已打日志的未知cmd"""


class HandlerInterface:
    """
    直播消息处理器接口
    """

    async def handle(self, client: client_.BLiveClient, command: dict):
        raise NotImplementedError


class BaseHandler(HandlerInterface):
    """
    一个简单的消息处理器实现，带消息分发和消息类型转换。继承并重写_on_xxx方法即可实现自己的处理器
    """

    def __heartbeat_callback(self, client: client_.BLiveClient, command: dict):
        return self._on_heartbeat(client, models.HeartbeatMessage.from_command(command['data']))

    def __danmu_msg_callback(self, client: client_.BLiveClient, command: dict):
        return self._on_danmaku(client, models.DanmakuMessage.from_command(command['info']))

    def __send_gift_callback(self, client: client_.BLiveClient, command: dict):
        return self._on_gift(client, models.GiftMessage.from_command(command['data']))

    def __guard_buy_callback(self, client: client_.BLiveClient, command: dict):
        return self._on_buy_guard(client, models.GuardBuyMessage.from_command(command['data']))

    def __super_chat_message_callback(self, client: client_.BLiveClient, command: dict):
        return self._on_super_chat(client, models.SuperChatMessage.from_command(command['data']))

    def __super_chat_message_delete_callback(self, client: client_.BLiveClient, command: dict):
        return self._on_super_chat_delete(client, models.SuperChatDeleteMessage.from_command(command['data']))

    _CMD_CALLBACK_DICT: Dict[
        str,
        Optional[Callable[
            ['BaseHandler', client_.BLiveClient, dict],
            Awaitable
        ]]
    ] = {
        # 收到心跳包，这是blivedm自造的消息，原本的心跳包格式不一样
        '_HEARTBEAT': __heartbeat_callback,
        # 收到弹幕
        # go-common\app\service\live\live-dm\service\v1\send.go
        'DANMU_MSG': __danmu_msg_callback,
        # 有人送礼
        'SEND_GIFT': __send_gift_callback,
        # 有人上舰
        'GUARD_BUY': __guard_buy_callback,
        # 醒目留言
        'SUPER_CHAT_MESSAGE': __super_chat_message_callback,
        # 删除醒目留言
        'SUPER_CHAT_MESSAGE_DELETE': __super_chat_message_delete_callback,
    }
    """cmd -> 处理回调"""
    # 忽略其他常见cmd
    for cmd in IGNORED_CMDS:
        _CMD_CALLBACK_DICT[cmd] = None
    del cmd

    async def handle(self, client: client_.BLiveClient, command: dict):
        cmd = command.get('cmd', '')
        pos = cmd.find(':')  # 2019-5-29 B站弹幕升级新增了参数
        if pos != -1:
            cmd = cmd[:pos]

        if cmd not in self._CMD_CALLBACK_DICT:
            # 只有第一次遇到未知cmd时打日志
            if cmd not in logged_unknown_cmds:
                logger.warning('room=%d unknown cmd=%s, command=%s', client.room_id, cmd, command)
                logged_unknown_cmds.add(cmd)
            return

        callback = self._CMD_CALLBACK_DICT[cmd]
        if callback is not None:
            await callback(self, client, command)

    async def _on_heartbeat(self, client: client_.BLiveClient, message: models.HeartbeatMessage):
        """
        收到心跳包（人气值）
        """

    async def _on_danmaku(self, client: client_.BLiveClient, message: models.DanmakuMessage):
        """
        收到弹幕
        """

    async def _on_gift(self, client: client_.BLiveClient, message: models.GiftMessage):
        """
        收到礼物
        """

    async def _on_buy_guard(self, client: client_.BLiveClient, message: models.GuardBuyMessage):
        """
        有人上舰
        """

    async def _on_super_chat(self, client: client_.BLiveClient, message: models.SuperChatMessage):
        """
        醒目留言
        """

    async def _on_super_chat_delete(self, client: client_.BLiveClient, message: models.SuperChatDeleteMessage):
        """
        删除醒目留言
        """
