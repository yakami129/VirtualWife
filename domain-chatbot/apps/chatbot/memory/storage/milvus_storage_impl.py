from .milvus.milvus_memory import MilvusMemory
from .base_storage import BaseStorage


class MilvusStorage(BaseStorage):
    '''Milvus向量存储记忆模块'''
    milvus_memory: MilvusMemory

    def __init__(self, storage_config: dict[str, str]):
        host = storage_config["host"]
        port = storage_config["port"]
        user = storage_config["user"]
        password = storage_config["password"]
        db_name = storage_config["db_name"]
        self.milvus_memory = MilvusMemory(
            host=host, port=port, user=user, password=password, db_name=db_name)

    def search(self, query_text: str, owner: str) -> list[str]:

        self.milvus_memory.loda()
        # 查询记忆，并且使用 关联性 + 重要性 + 最近性 算法进行评分
        memories = self.milvus_memory.compute_relevance(query_text, owner)
        self.milvus_memory.compute_importance(memories)
        self.milvus_memory.compute_recency(memories)
        self.milvus_memory.normalize_scores(memories)
        self.milvus_memory.release()

        # 排序获得最高分的记忆
        memories = sorted(
            memories, key=lambda m: m["total_score"], reverse=True)
        return memories[0]

    def save(self, quer_text: str, owner: str) -> None:
        self.milvus_memory.loda()
        self.milvus_memory.insert_memory(text=quer_text, owner=owner)
        self.milvus_memory.release()

    def clear(self, owner: str) -> None:
        self.milvus_memory.loda()
        self.milvus_memory.clear(owner)
        self.milvus_memory.release()
