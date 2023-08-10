from .milvus_storage_impl import MilvusStorage
from .local_storage_impl import LocalStorage
from .base_storage import BaseStorage


class StorageDriver():

    strategy: BaseStorage

    def __init__(self, type: str, storage_config: dict[str, str]) -> None:
        if type == 'local':
            self.strategy = LocalStorage(storage_config)
        elif type == 'milvus':
            self.strategy = MilvusStorage(storage_config)
        else:
            raise ValueError("Unknown type")

    def search(self, query_text: str, owner: str) -> list[str]:
        return self.strategy.search(query_text, owner)

    def save(self, query_text: str, owner: str) -> None:
        return self.strategy.save(query_text, owner)

    def clear(self, owner: str) -> None:
        return self.strategy.clear(owner)