import datetime
import jieba
import jieba.analyse
from django.db.models import Q
from ..base_storage import BaseStorage
from ...models import LocalMemoryModel


class LocalStorage(BaseStorage):

    def __init__(self, memory_storage_config: dict[str, str]):
        print("========================load LocalStorage ========================")

    def search(self, query_text: str, limit: int, owner: str) -> list[str]:

        query_words = jieba.cut(query_text, cut_all=False)
        query_tags = list(query_words)
        keywords = jieba.analyse.extract_tags(" ".join(query_tags), topK=20)

        # 使用 Q 对象组合查询条件，
        query = Q(owner=owner)
        for keyword in keywords:
            query |= Q(tags__icontains=keyword)  # 使用 | 运算符将多个条件组合在一起

        # 查询结果，并限制数量
        results = LocalMemoryModel.objects.filter(
            query).order_by('-timestamp')[:limit]

        # 提取查询结果的 text 字段
        result_texts = [result.text for result in results]
        return result_texts

    def pageQuery(self, page_num: int, page_size: int, owner: str) -> list[str]:
        # 计算分页偏移量
        offset = (page_num - 1) * page_size

        # 分页查询，并提取 text 字段
        results = LocalMemoryModel.objects.filter(owner=owner).order_by('-timestamp').values_list(
            'text', flat=True)[offset:offset + page_size]
        return list(results)

    def save(self, pk: int, query_text: str, owner: str, importance_score: int) -> None:
        query_words = jieba.cut(query_text, cut_all=False)
        query_tags = list(query_words)
        keywords = jieba.analyse.extract_tags(" ".join(query_tags), topK=20)
        current_timestamp = datetime.datetime.now().isoformat()  #
        local_memory_model = LocalMemoryModel(
            id=pk,
            text=query_text,
            tags=",".join(keywords),  # 设置标签
            owner=owner,
            timestamp=current_timestamp
        )
        local_memory_model.save()

    def clear(self, owner: str) -> None:
        # 清除指定 owner 的记录
        LocalMemoryModel.objects.filter(owner=owner).delete()
