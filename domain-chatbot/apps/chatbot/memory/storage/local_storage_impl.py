from .base_storage import BaseStorage


class LocalStorage(BaseStorage):
    '''本地存储记忆模块'''

    def search(self, query_text: str, limit: int, expr: str == None) -> list[str]:
        return ["TODO"]

    def pageQuery(self, page_num: int, page_size: int, expr: str) -> list[str]:
        '''分页检索记忆'''
        return ["TODO"]

    def save(self, pk: int,  quer_text: str, owner: str) -> None:
        return "TODO"

    def clear(self, owner: str) -> None:
        t = "TODO"
