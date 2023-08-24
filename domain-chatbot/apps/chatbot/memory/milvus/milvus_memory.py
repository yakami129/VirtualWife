# 导入所需模块
import os
from ...utils.snowflake_utils import SnowFlake
from pymilvus import DataType, FieldSchema, CollectionSchema, Collection, connections
from sentence_transformers import SentenceTransformer
import time


_COLLECTION_NAME = "virtual_wife_memory"
os.environ["TOKENIZERS_PARALLELISM"] = "false" 


class MilvusMemory():

    collection: Collection
    schema: CollectionSchema
    model: SentenceTransformer
    snow_flake: SnowFlake

    def __init__(self, host: str, port: str, user: str, password: str, db_name: str):

        connections.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            db_name=db_name,
        )

        # 定义记忆Stream集合schema、创建记忆Stream集合
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=2000),
            FieldSchema(name="owner", dtype=DataType.VARCHAR, max_length=50),
            FieldSchema(name="timestamp", dtype=DataType.DOUBLE),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR,
                        dim=384),  # 文本embedding向量
        ]
        self.schema = CollectionSchema(fields, _COLLECTION_NAME)
        self.collection = Collection(_COLLECTION_NAME, self.schema)

        # 创建索引
        index = {
            "index_type": "IVF_SQ8",
            "metric_type": "L2",
            "params": {"nlist": 384},
        }
        self.collection.create_index("embedding", index)

        # 初始化向量化模型
        self.model = SentenceTransformer(
            'sentence-transformers/all-MiniLM-L6-v2')

    def get_embedding_from_language_model(self, text: str):
        embedding = self.model.encode(text)
        return embedding

    def get_importance_score_from_language_model(self, text: str, chat_fun=None):
        '''通过大语言模型计算记忆重要程度'''
        importance_score = 1
        if chat_fun != None:
            importance_score = chat_fun.chat(str)
        return importance_score

    def insert_memory(self, pk: int,  text: str, owner: str):
        '''定义插入记忆对象函数'''
        timestamp = time.time()

        # 使用语言模型获得文本embedding向量
        embedding = self.get_embedding_from_language_model(text)
        data = [[pk], [text], [owner], [timestamp], [embedding]]
        self.collection.insert(data)

    def compute_relevance(self, query_text: str, limit: int, expr: str == None):
        '''定义计算相关性分数函数'''

        # 搜索表达式
        search_result = self.search_memory(
            query_text, limit, expr)
        hits = []
        for hit in search_result:
            memory = {
                "id": hit.entity.id,
                "text": hit.entity.text,
                "timestamp": hit.entity.timestamp,
                "owner": hit.entity.owner
            }
            memory["relevance"] = 1 - hit.distance
            hits.append(memory)

        return hits

    def search_memory(self, query_text: str, limit: int, expr: str == None):

        query_embedding = self.get_embedding_from_language_model(query_text)
        search_params = {"metric_type": "L2", "params": {"nprobe": 30}}

        # 搜索向量关联的最新30条记忆
        vector_hits = None
        if expr != None:
            vector_hits = self.collection.search(
                data=[query_embedding],
                anns_field="embedding",
                param=search_params,
                limit=limit,
                expr=expr,
                output_fields=["id", "text", "owner", "timestamp"]
            )
        else:
            vector_hits = self.collection.search(
                data=[query_embedding],
                anns_field="embedding",
                param=search_params,
                limit=limit,
                output_fields=["id", "text", "owner", "timestamp"]
            )

        return vector_hits[0]

    def compute_importance(self, memories):
        '''定义计算重要性分数函数'''
        for memory in memories:
            # 使用语言模型评分文本的重要性
            memory["importance"] = self.get_importance_score_from_language_model(
                memory["text"])

    def compute_recency(self, memories):
        '''定义计算最近性分数函数'''
        current_time = time.time()
        for memory in memories:
            time_diff = current_time - memory["timestamp"]
            memory["recency"] = 0.99 ** (time_diff / 3600)  # 指数衰减

    def normalize_scores(self, memories):
        for memory in memories:
            memory["total_score"] = memory["relevance"] + \
                memory["importance"] + memory["recency"]

    def pageQuery(self, expr: str, offset: int, limit: int):
        vector_hits = self.collection.query(
            expr=expr,
            offset=offset,
            limit=limit,
            output_fields=["id", "text", "owner", "timestamp"]
        )
        return vector_hits

    def loda(self):
        self.collection.load()

    def release(self):
        self.collection.release()

    def clear(self, owner: str):
        ids_result = self.collection.query(
            expr=f"owner !=''",
            offset=0,
            limit=100,
            output_fields=["id"])
        ids = [item['id'] for item in ids_result]
        ids_expr = f"id in {ids}"
        self.collection.delete(ids_expr)

    # if __name__ == "__main__":

    #     # 测试代码
    #     insert_memory("John ate breakfast this morning", "John")
    #     insert_memory("Mary is planning a party for Valentine's Day", "John")
    #     insert_memory("John likes to eat BBQ", "John")
    #     insert_memory("Alan likes to eat TV", "Alan")
    #     insert_memory("Alan likes to eat Macbook", "Alan")
    #     insert_memory("John went to the library in the morning", "John")

    #     # query_text = "What are John's plans for today?"
    #     query_text = "What does Alan like?"

    #     collection.load()

    #     memories = compute_relevance(query_text, "Alan")

    #     compute_importance(memories)
    #     compute_recency(memories)
    #     normalize_scores(memories)
    #     print(memories)

    #     print("Retrieved memories:")
    #     for memory in sorted(memories, key=lambda m: m["total_score"], reverse=True)[:5]:
    #         print(memory["text"], ", total score:", memory["total_score"])

    #     # 清楚原数据
    #     utility.drop_collection("memory_stream_test11")
