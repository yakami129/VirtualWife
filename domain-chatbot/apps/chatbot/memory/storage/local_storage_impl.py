from .base_storage import BaseStorage


class LocalStorage(BaseStorage):
    '''本地存储记忆模块'''

    def search(self, query_text: str, owner: str) -> list[str]:
        return ["TODO"]

    def save(self, quer_text: str, owner: str) -> None:
        return "TODO"

    def clear(self, owner: str) -> None:
        t = "TODO"
