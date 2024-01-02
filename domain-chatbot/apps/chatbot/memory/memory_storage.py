import logging

from .zep.zep_memory import ChatHistroyService, ChatHistroy
from typing import Any, Dict, List

from ..service import portal_user_service

logger = logging.getLogger(__name__)


class MemoryStorageDriver:
    chat_histroy_service: ChatHistroyService
    enable_long_memory: bool
    search_memory_size: int

    def __init__(self, zep_url: str, zep_optional_api_key: str, search_memory_size: int,
                 enable_long_memory: bool) -> None:
        self.chat_histroy_service = ChatHistroyService(
            zep_url, zep_optional_api_key)
        self.enable_long_memory = enable_long_memory
        self.search_memory_size = search_memory_size

    def search_short_memory(self, query_text: str, you_name: str, role_name: str) -> list[ChatHistroy]:
        portal_user = portal_user_service.get_and_create(you_name)
        user_id = str(portal_user.id)
        channel_id = str(portal_user.id)
        return self.chat_histroy_service.list(user_id=user_id, channel_id=channel_id)

    def search_lang_memory(self, query_text: str, you_name: str, role_name: str) -> str:
        if self.enable_long_memory:
            portal_user = portal_user_service.get_and_create(you_name)
            user_id = str(portal_user.id)
            channel_id = str(portal_user.id)
            # 查询长期记忆
            chat_histroys = self.chat_histroy_service.search(query=query_text, user_id=user_id, channel_id=channel_id,
                                                             limit=self.search_memory_size)
            chat_histroy_str = []
            for item in chat_histroys:
                chat_histroy_str.append(item.content)
            lang_memory = ";\n".join(chat_histroy_str)
            # 查询当前人物画像数据
            user = self.chat_histroy_service.zep_service.get_user(user_id)
            portrait = ""
            if user:
                portrait = user.metadata["portrait"]
            return portrait + ";\n" + lang_memory
        else:
            return "无"

    def save(self, you_name: str, query_text: str, role_name: str, answer_text: str) -> None:
        portal_user = portal_user_service.get_and_create(you_name)
        user_id = str(portal_user.id)
        channel_id = str(portal_user.id)
        self.chat_histroy_service.push(user_id=user_id, user_name=you_name, channel_id=channel_id, chat_histroy=ChatHistroy(role="ai",
                                                                                                                            content=self.__format_role_history(
                                                                                                                                role_name=role_name,
                                                                                                                                answer_text=answer_text)))
        self.chat_histroy_service.push(user_id=user_id, user_name=you_name, channel_id=channel_id, chat_histroy=ChatHistroy(role="human",
                                                                                                                            content=self.__format_you_history(
                                                                                                                                you_name=you_name,
                                                                                                                                query_text=query_text)))

    def format_history(self, you_name: str, query_text: str, role_name: str, answer_text: str):
        you_history = self.__format_you_history(
            you_name=you_name, query_text=query_text)
        role_history = self.__format_role_history(
            role_name=role_name, answer_text=answer_text)
        chat_history = you_history + ';' + role_history
        return chat_history

    def __format_you_history(self, you_name: str, query_text: str):
        you_history = f"{you_name}说{query_text}"
        return you_history

    def __format_role_history(self, role_name: str, answer_text: str):
        role_history = f"{role_name}说{answer_text}"
        return role_history

    def clear(self, owner: str) -> None:
        self.long_memory_storage.clear(owner)
        self.short_memory_storage.clear(owner)
