import logging

from .zep.zep_memory import ChatHistroyService, ChatHistroy
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class MemoryStorageDriver:
    chat_histroy_service: ChatHistroyService
    enable_longMemory: bool

    def __init__(self, zep_url: str, zep_optional_api_key: str, search_memory_size: str,
                 enable_longMemory: bool) -> None:
        self.chat_histroy_service = ChatHistroyService(zep_url, zep_optional_api_key, search_memory_size)
        self.enable_longMemory = enable_longMemory

    def search_short_memory(self, query_text: str, you_name: str, role_name: str) -> list[ChatHistroy]:
        user_id = you_name
        channel_id = you_name
        return self.chat_histroy_service.list(user_id=user_id, channel_id=channel_id)

    def search_lang_memory(self, query_text: str, you_name: str, role_name: str) -> str:
        if self.enable_longMemory:
            user_id = you_name
            channel_id = you_name
            self.chat_histroy_service.search(user_id=user_id, channel_id=channel_id)
            return ""
        else:
            return "无"

    def save(self, you_name: str, query_text: str, role_name: str, answer_text: str) -> None:
        user_id = you_name
        channel_id = you_name
        self.chat_histroy_service.push(user_id=user_id, channel_id=channel_id, chat_histroy=ChatHistroy(role="ai",
                                                                                                        content=self.__format_role_history(
                                                                                                            role_name=role_name,
                                                                                                            answer_text=answer_text)))
        self.chat_histroy_service.push(user_id=user_id, channel_id=channel_id, chat_histroy=ChatHistroy(role="human",
                                                                                                        content=self.__format_you_history(
                                                                                                            you_name=you_name,
                                                                                                            query_text=query_text)))

    def __format_history(self, you_name: str, query_text: str, role_name: str, answer_text: str):
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
