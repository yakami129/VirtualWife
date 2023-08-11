import numpy as np
from langchain.memory import ConversationBufferWindowMemory
from .milvus_storage_impl import MilvusStorage
from .local_storage_impl import LocalStorage
from .base_storage import BaseStorage


class MemoryStorageDriver():

    strategy: BaseStorage
    tmp_memory_dict: dict[str, ConversationBufferWindowMemory] = {}
    tmp_k_num: int = 5

    def __init__(self, type: str, memory_storage_config: dict[str, str]) -> None:
        if type == 'local':
            self.strategy = LocalStorage(memory_storage_config)
        elif type == 'milvus':
            self.strategy = MilvusStorage(memory_storage_config)
        else:
            raise ValueError("Unknown type")

    def search(self, query_text: str, owner: str) -> list[str]:

        # 获取短期记忆
        tmp_memory_dict = self.tmp_memory_dict.get(owner, None)
        tmp_memory = []
        if tmp_memory_dict != None:
            tmp_memory_item = tmp_memory_dict.load_memory_variables({})[
                "history"]
            tmp_memory.append(tmp_memory_item)
        tmp_memory = np.array(tmp_memory)

        # 获取长期记忆
        long_term_memory = np.array(self.strategy.search(query_text, owner))
        comprehensive_memory = np.concatenate([tmp_memory, long_term_memory])
        return comprehensive_memory

    def save(self, role_name: str, you_name: str, query_text: str, answer_text: str) -> None:
        you_history = f"{you_name}:{query_text}"
        role_history = f"{role_name}:{answer_text}"
        history = you_history + '\n' + role_history

        # 获取短期记忆存储对象，如果没有创建新的
        tmp_memory_dict = self.tmp_memory_dict.get(you_name, None)
        if tmp_memory_dict == None:
            new_tmp_memory_dict = ConversationBufferWindowMemory(
                k=self.tmp_k_num, human_prefix=you_name, ai_prefix=role_name)
            self.tmp_memory_dict[you_name] = new_tmp_memory_dict
            tmp_memory_dict = new_tmp_memory_dict

        tmp_memory_dict.save_context({"input": query_text}, {
            "output": answer_text})

        return self.strategy.save(history, you_name)

    def clear(self, owner: str) -> None:
        return self.strategy.clear(owner)
