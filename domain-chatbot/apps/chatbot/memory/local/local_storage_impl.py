import datetime
import logging
import jieba
import jieba.analyse
import json
from django.db.models import Q
from ..base_storage import BaseStorage
from ...models import LocalMemoryModel

# TODO 搜索方式待整改
logger = logging.getLogger(__name__)


class LocalStorage(BaseStorage):

    def __init__(self, memory_storage_config: dict[str, str]):
        logger.info("=> Load LocalStorage Success")

    def search(self, query_text: str, limit: int, owner: str) -> list[str]:
        # 使用 Q 对象组合查询条件，
        query = Q(owner=owner)

        # 查询结果，并限制数量
        results = LocalMemoryModel.objects.filter(
            query).order_by('-timestamp')[:limit]

        # 提取查询结果的 text 字段
        result_texts = [result.text for result in results]
        return result_texts

    def pageQueryByOwner(self, page_num: int, page_size: int, owner: str) -> list[str]:
        # 计算分页偏移量
        offset = (page_num - 1) * page_size

        # 分页查询，并提取 text 字段
        results = LocalMemoryModel.objects.filter(owner=owner).order_by('-timestamp').values_list(
            'text', flat=True)[offset:offset + page_size]
        results = list(results)
        results.reverse()
        return results

    def pageQuery(self, page_num: int, page_size: int) -> list[str]:
        # 计算分页偏移量
        offset = (page_num - 1) * page_size

        # 分页查询，并提取 text 字段
        results = LocalMemoryModel.objects.order_by('-timestamp').values_list(
            'text', flat=True)[offset:offset + page_size]
        results = list(results)
        results.reverse()
        return results

    def save(self, pk: int, query_text: str, sender: str, owner: str, importance_score: int) -> None:
        query_words = jieba.cut(query_text, cut_all=False)
        query_tags = list(query_words)
        keywords = jieba.analyse.extract_tags(" ".join(query_tags), topK=20)
        current_timestamp = datetime.datetime.now().isoformat()  #
        local_memory_model = LocalMemoryModel(
            id=pk,
            text=query_text,
            tags=",".join(keywords),  # 设置标签
            sender=sender,
            owner=owner,
            timestamp=current_timestamp
        )
        local_memory_model.save()

    def clear(self, owner: str) -> None:
        # 清除指定 owner 的记录
        LocalMemoryModel.objects.filter(owner=owner).delete()
