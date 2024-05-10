import json
import logging
import traceback

from ..config.sys_config import SysConfig
from .milvus.milvus_storage_impl import MilvusStorage
from .local.local_storage_impl import LocalStorage
from ..utils.snowflake_utils import SnowFlake
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class MemoryStorageDriver:
    sys_config: SysConfig
    short_memory_storage: LocalStorage
    long_memory_storage: MilvusStorage
    snow_flake: SnowFlake = SnowFlake(data_center_id=5, worker_id=5)

    def __init__(self, memory_storage_config: dict[str, str], sys_config: SysConfig) -> None:
        self.sys_config = sys_config
        self.short_memory_storage = LocalStorage(memory_storage_config)
        if sys_config.enable_longMemory:
            self.long_memory_storage = MilvusStorage(memory_storage_config)

    def search_short_memory(self, query_text: str, you_name: str, role_name: str) -> list[Dict[str, str]]:
        local_memory = self.short_memory_storage.pageQuery(
            page_num=1, page_size=self.sys_config.local_memory_num)
        dict_list = []
        for json_string in local_memory:
            json_dict = json.loads(json_string)
            dict_list.append(json_dict)
        return dict_list

    def search_lang_memory(self, query_text: str, you_name: str, role_name: str) -> str:
        if self.sys_config.enable_longMemory:
            try:
                # 获取长期记忆，按照角色划分
                long_memory = self.long_memory_storage.search(
                    query_text, 3, sender=you_name, owner=role_name)
                long_history = ""
                summary_historys = []
                if len(long_memory) > 0:
                    # 将json字符串转换为字典
                    for i in range(len(long_memory)):
                        summary_historys.append(long_memory[i])
                    long_history = ";".join(summary_historys)
                return long_history
            except Exception as e:
                traceback.print_exc()
                logger.error("chat error: %s" % str(e))
            return ""
        else:
            return ""

    def save(self, you_name: str, query_text: str, role_name: str, answer_text: str) -> None:

        # 存储短期记忆
        pk = self.get_current_entity_id()
        local_history = {
            "ai": self.__format_role_history(role_name=role_name, answer_text=answer_text),
            "human": self.__format_you_history(you_name=you_name, query_text=query_text)
        }
        self.short_memory_storage.save(
            pk, json.dumps(local_history), you_name, role_name, importance_score=1)

        # 是否开启长期记忆
        if self.sys_config.enable_longMemory:
            # 将当前对话语句生成摘要
            history = self.format_history(
                you_name=you_name, query_text=query_text, role_name=role_name, answer_text=answer_text)
            importance_score = 3
            if self.sys_config.enable_summary:
                memory_summary = MemorySummary(self.sys_config)
                history = memory_summary.summary(
                    llm_model_type=self.sys_config.summary_llm_model_driver_type, input=history)
                # 计算记忆的重要程度
                memory_importance = MemoryImportance(self.sys_config)
                importance_score = memory_importance.importance(
                    self.sys_config.summary_llm_model_driver_type, input=history)
            self.long_memory_storage.save(
                pk, history, you_name, role_name, importance_score)

    def format_history(self, you_name: str, query_text: str, role_name: str, answer_text: str):
        you_history = self.__format_you_history(
            you_name=you_name, query_text=query_text)
        role_history = self.__format_role_history(
            role_name=role_name, answer_text=answer_text)
        chat_history = you_history + ';' + role_history
        return chat_history

    def __format_you_history(self, you_name: str, query_text: str):
        you_history = f"{you_name}说{query_text}"
        return you_history

    def __format_role_history(self, role_name: str, answer_text: str):
        role_history = f"{role_name}说{answer_text}"
        return role_history

    def get_current_entity_id(self) -> int:
        '''生成唯一标识'''
        return self.snow_flake.task()

    def clear(self, owner: str) -> None:
        self.long_memory_storage.clear(owner)
        self.short_memory_storage.clear(owner)


class MemorySummary:
    sys_config: SysConfig
    prompt: str

    def __init__(self, sys_config: SysConfig) -> None:
        self.sys_config = sys_config
        self.prompt = '''
               <s>[INST] <<SYS>>          
                Please help me extract key information about the content of the conversation, here is an example of extracting key information:
                input:"alan说你好，爱莉，很高兴认识你，我是一名程序员，我喜欢吃川菜，;爱莉说我们是兼容的
                output:{"summary"："alan向爱莉表示自己是一名程序员，alan喜欢吃川菜，爱莉认为和alan是兼容的"}
                Please export the conversation summary in Chinese.
                Please use JSON format strictly and output the result:
                {"Summary": "A summary of the conversation you generated"}
                <</SYS>>
        '''

    def summary(self, llm_model_type: str, input: str) -> str:
        result = self.sys_config.llm_model_driver.chat(prompt=self.prompt, type=llm_model_type, role_name="",
                                                       you_name="", query=f"input:{input}", short_history=[],
                                                       long_history="")
        logger.debug("=> summary:", result)
        summary = input
        if result:
            # 寻找 JSON 子串的开始和结束位置
            start_idx = result.find('{')
            end_idx = result.rfind('}')
            if start_idx != -1 and end_idx != -1:
                json_str = result[start_idx:end_idx + 1]
                json_data = json.loads(json_str)
                summary = json_data["Summary"]
            else:
                logger.warn("未找到匹配的JSON字符串")
        return summary


class MemoryImportance:
    sys_config: SysConfig
    prompt: str

    def __init__(self, sys_config: SysConfig) -> None:
        self.sys_config = sys_config
        self.prompt = '''
               <s>[INST] <<SYS>>  
                There is a scoring mechanism for the importance of memory, on a scale of 10, where 1 is a mundane task (eg, brushing your teeth, making your bed) and 10 is an impressive extremely and important task (eg, breaking up, college admissions), Please help me evaluate the importance score of the following memory.
                Please do not output the inference process, just output the scoring results.
                Please output the results strictly in JSON format:
                {"score": "The rating result you generated"}
                <</SYS>>
        '''

    def importance(self, llm_model_type: str, input: str) -> int:
        result = self.sys_config.llm_model_driver.chat(prompt=self.prompt, type=llm_model_type, role_name="",
                                                       you_name="", query=f"memory:{input}", short_history=[],
                                                       long_history="")
        logger.debug("=> score:", result)
        # 寻找 JSON 子串的开始和结束位置
        start_idx = result.find('{')
        end_idx = result.rfind('}')
        score = 3
        if start_idx != -1 and end_idx != -1:
            json_str = result[start_idx:end_idx + 1]
            json_data = json.loads(json_str)
            score = int(json_data["score"])
        else:
            logger.warn("未找到匹配的JSON字符串")
        return score
