import json
from typing import Tuple

from ..config.sys_config import SysConfig
from typing import List
from .milvus.milvus_storage_impl import MilvusStorage
from .local.local_storage_impl import LocalStorage
from .base_storage import BaseStorage
from ..utils.snowflake_utils import SnowFlake
from typing import Any, Dict, List


class MemoryStorageDriver():

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
            page_num=1, page_size=self.sys_config.local_memory_num, owner=role_name)
        dict_list = []
        for json_string in local_memory:
            json_dict = json.loads(json_string)
            dict_list.append(json_dict)
        return dict_list

    def search_lang_memory(self, query_text: str, you_name: str, role_name: str) -> str:
        if self.sys_config.enable_longMemory:
            # 获取长期记忆，按照角色划分
            long_memory = self.long_memory_storage.search(
                query_text, 3, owner=role_name)
            long_history = ""
            summary_historys = []
            if len(long_memory) > 0:
                # 将json字符串转换为字典
                for i in range(len(long_memory)):
                    summary_historys.append(long_memory[i])
                long_history = ";".join(summary_historys)
            return long_history
        else:
            return ""

    def save(self,  you_name: str, query_text: str, role_name: str, answer_text: str) -> None:

        # 存储短期记忆
        pk = self.get_current_entity_id()
        local_history = {
            "ai": self.format_role_history(role_name=role_name, answer_text=answer_text),
            "human": self.format_you_history(you_name=you_name, query_text=query_text)
        }
        self.short_memory_storage.save(
            pk, json.dumps(local_history), role_name, importance_score=1)

        # 是否开启长期记忆
        if self.sys_config.enable_longMemory:
            # 将当前对话语句生成摘要
            history = self.format_history(
                you_name=you_name, query_text=query_text, role_name=role_name, answer_text=answer_text)
            importance_score = 3
            if self.sys_config.enable_summary:
                memory_summary = MemorySummary(self.sys_config)
                summary = memory_summary.summary(
                    llm_model_type=self.sys_config.summary_llm_model_driver_type, input=history)
                history = summary["summary"]
                # 计算记忆的重要程度
                memory_importance = MemoryImportance(self.sys_config)
                importance_score = memory_importance.importance(
                    self.sys_config.summary_llm_model_driver_type, input=history)
            self.long_memory_storage.save(
                pk, history, role_name, importance_score)

    def format_history(self, you_name: str, query_text: str, role_name: str, answer_text: str):
        you_history = self.format_you_history(
            you_name=you_name, query_text=query_text)
        role_history = self.format_role_history(
            role_name=role_name, answer_text=answer_text)
        chat_history = you_history + ';' + role_history
        return chat_history

    def format_you_history(self, you_name: str, query_text: str):
        you_history = f"{you_name}说{query_text}"
        return you_history

    def format_role_history(self, role_name: str, answer_text: str):
        role_history = f"{role_name}说{answer_text}"
        return role_history

    def get_current_entity_id(self) -> int:
        '''生成唯一标识'''
        return self.snow_flake.task()

    def clear(self, owner: str) -> None:
        self.long_memory_storage.clear(owner)
        self.short_memory_storage.clear(owner)


class MemorySummary():

    sys_config: SysConfig
    prompt: str

    def __init__(self, sys_config: SysConfig) -> None:
        self.sys_config = sys_config
        self.prompt = '''
               <s>[INST] <<SYS>>          
                请帮我提取对话内容的关键信息，下面是一个提取关键信息的示例:
                ```
                input:"alan说你好，爱莉，很高兴认识你，我是一名程序员，我喜欢吃川菜，也喜欢打篮球，我是水瓶座，生日是1月29日;爱莉说我们是兼容的
                output:{"summary"："alan向爱莉表示自己是一名程序员，alan喜欢吃川菜和打篮球，alan是水瓶座，生日是1月29日，爱莉认为和alan是兼容的"}
                ```
                输出格式请严格使用JSON格式：
                ```
                {"summary":"对话摘要"}
                ```
                <</SYS>>
        '''

    def summary(self, llm_model_type: str, input: str) -> str:
        prompt = self.prompt + f"input:{input} [/INST]"
        result = self.sys_config.llm_model_driver.chat(prompt=prompt, type=llm_model_type, role_name="",
                                                       you_name="", query=input, short_history="", long_history="")
        print("=> summary:", result)
        # 寻找 JSON 子串的开始和结束位置
        start_idx = result.find('{')
        end_idx = result.rfind('}')
        if start_idx != -1 and end_idx != -1:
            json_str = result[start_idx:end_idx+1]
            json_data = json.loads(json_str)
        else:
            json_data = {}
            print("未找到匹配的JSON字符串")
        return json_data


class MemoryImportance():

    sys_config: SysConfig
    prompt: str

    def __init__(self, sys_config: SysConfig) -> None:
        self.sys_config = sys_config
        self.prompt = '''
               <s>[INST] <<SYS>>  
                有一种记忆重要程度的评分机制，在到10的范围内，其中1是平凡的事务（例如，刷牙、铺床），10是极其印象深刻切重要的事务（例如，分手、大学录取），请帮我评估下面一段记忆的重要程度分数
                输出格式请严格使用JSON格式：
                ```
                {"score":"评分整数"}
                ```
                <</SYS>>
        '''

    def importance(self, llm_model_type: str, input: str) -> int:
        prompt = self.prompt + f"记忆:{input} [/INST]"
        result = self.sys_config.llm_model_driver.chat(prompt=prompt, type=llm_model_type, role_name="",
                                                       you_name="", query=input, short_history="", long_history="")
        print("=> importance:", result)
        # 寻找 JSON 子串的开始和结束位置
        start_idx = result.find('{')
        end_idx = result.rfind('}')
        score = 3
        if start_idx != -1 and end_idx != -1:
            json_str = result[start_idx:end_idx+1]
            json_data = json.loads(json_str)
            score = int(json_data["score"])
        else:
            print("未找到匹配的JSON字符串")
        return score
