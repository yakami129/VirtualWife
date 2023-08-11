from .milvus_storage_impl import MilvusStorage
from .local_storage_impl import LocalStorage
from .base_storage import BaseStorage


class MemoryStorageDriver():

    strategy: BaseStorage

    def __init__(self, type: str, memory_storage_config: dict[str, str]) -> None:
        if type == 'local':
            self.strategy = LocalStorage(memory_storage_config)
        elif type == 'milvus':
            self.strategy = MilvusStorage(memory_storage_config)
        else:
            raise ValueError("Unknown type")

    def search(self, query_text: str, owner: str) -> list[str]:
        return self.strategy.search(query_text, owner)

    def save(self, role_name: str, you_name: str, query_text: str, answer_text: str) -> None:
        you_history = f"{you_name}:{query_text}"    
        role_history = f"{role_name}:{answer_text}"    
        history = you_history + '\n' + role_history
        print("history:",history)
        return self.strategy.save(history, you_name)

    def clear(self, owner: str) -> None:
        return self.strategy.clear(owner)
