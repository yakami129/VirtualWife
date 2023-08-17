from .base_storage import BaseStorage
from langchain.memory import ConversationBufferWindowMemory


class LocalStorage(BaseStorage):

    '''本地存储记忆模块'''
    short_memory_dict: dict[str, ConversationBufferWindowMemory] = {}

    def __init__(self, memory_storage_config: dict[str, str]):
        print("")

    def search(self, query_text: str, limit: int, expr: str == None) -> list[str]:
        return []

    def pageQuery(self, page_num: int, page_size: int, expr: str) -> list[str]:
        '''分页检索记忆'''
        return []

    def save(self, pk: int,  quer_text: str, owner: str) -> None:
        '''保存记忆'''
        return None

    def clear(self, owner: str) -> None:
        t = "TODO"
