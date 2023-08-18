import re
import json
from typing import Tuple

from ...config.sys_config import SysConfig
import numpy as np
from typing import List
from langchain.memory import ConversationBufferWindowMemory
from .milvus_storage_impl import MilvusStorage
from .local_storage_impl import LocalStorage
from .base_storage import BaseStorage
from ...utils.snowflake_utils import SnowFlake
from typing import Any, Dict, List
from langchain.memory.chat_memory import BaseChatMemory
from langchain.schema import BaseMessage
from langchain.schema import (
    HumanMessage,
    AIMessage,
    SystemMessage,
    ChatMessage
)


class WVConversationBufferWindowMemory(BaseChatMemory):
    """Buffer for storing conversation memory."""

    human_prefix: str = "Human"
    ai_prefix: str = "AI"
    memory_key: str = "history"  #: :meta private:
    k: int = 5

    @property
    def buffer(self) -> List[BaseMessage]:
        """String buffer of memory."""
        return self.chat_memory.messages

    @property
    def memory_variables(self) -> List[str]:
        """Will always return list of memory variables.

        :meta private:
        """
        return [self.memory_key]

    def load_memory_variables(self, inputs: Dict[str, Any], sysConfig: SysConfig) -> Dict[str, str]:
        """Return history buffer."""

        buffer: Any = self.buffer[-self.k * 2:] if self.k > 0 else []
        if not self.return_messages:
            buffer = self.get_buffer_string(
                buffer,
                human_prefix=self.human_prefix,
                ai_prefix=self.ai_prefix,
            )
        return {self.memory_key: buffer}

    def get_buffer_string(self, messages: List[BaseMessage], human_prefix: str = "Human", ai_prefix: str = "AI"
                          ) -> str:
        """Get buffer string of messages."""
        string_messages = []
        for m in messages:
            if isinstance(m, HumanMessage):
                role = human_prefix
            elif isinstance(m, AIMessage):
                role = ai_prefix
            elif isinstance(m, SystemMessage):
                role = "System"
            elif isinstance(m, ChatMessage):
                role = m.role
            else:
                raise ValueError(f"Got unsupported message type: {m}")
            string_messages.append(f"{role}:{m.content}")
        return ";".join(string_messages)


class MemoryStorageDriver():

    sysConfig: SysConfig
    strategy: BaseStorage
    short_memory_dict: dict[str, WVConversationBufferWindowMemory] = {}
    tmp_k_num: int = 5
    snow_flake: SnowFlake = SnowFlake(data_center_id=5, worker_id=5)

    def __init__(self, type: str, memory_storage_config: dict[str, str], sysConfig: SysConfig) -> None:
        self.sysConfig = sysConfig
        if type == 'local':
            self.strategy = LocalStorage(memory_storage_config)
        elif type == 'milvus':
            self.strategy = MilvusStorage(memory_storage_config)
        else:
            raise ValueError("Unknown type")

    def search(self, query_text: str, owner: str) -> Tuple[str, str]:

        # 获取短期记忆
        short_memory_dict = self.short_memory_dict.get(owner, None)
        short_memory = []
        short_history = ""
        if short_memory_dict != None:
            short_memory_item = short_memory_dict.load_memory_variables(inputs={}, sysConfig=self.sysConfig)[
                "history"]
            short_memory.append(short_memory_item)
        if len(short_memory) > 0:
            short_history = "\n".join(short_memory)

        # 获取长期记忆
        memory_query = f"{owner}：{query_text}"
        long_memory = self.strategy.search(memory_query, 30, expr=None)
        long_history = "[暂无长期记忆]"
        summary_historys = []
        if len(long_memory) > 0:
            # 将json字符串转换为字典
            for i in range(len(long_memory)):
                # 每个元素mem才是json字符串
                mem = long_memory[i]
                mem_dict = json.loads(mem)
                # 提取所有summary_history字段
                summary_historys.append(mem_dict['summary'])
            long_history = ";".join(summary_historys)
        return (short_history, long_history)

    def pageQuery(self, page_num: int, page_size: int, expr: str) -> list[str]:
        '''分页检索记忆'''
        return self.strategy.pageQuery(page_num=page_num, page_size=page_size, expr=expr)

    def save(self, role_name: str, you_name: str, query_text: str, answer_text: str) -> None:

        pk = self.get_current_entity_id()

        # 获取短期记忆存储对象，如果没有创建新的
        short_memory_dict = self.short_memory_dict.get(you_name, None)
        if short_memory_dict == None:
            new_short_memory_dict = WVConversationBufferWindowMemory(
                k=self.tmp_k_num, human_prefix=you_name, ai_prefix=role_name)
            self.short_memory_dict[you_name] = new_short_memory_dict
            short_memory_dict = new_short_memory_dict

        short_memory_dict.save_context({"input": query_text}, {
            "output": answer_text})

        # 将当前对话语句生成摘要，存储为长期记忆
        you_history = f"{you_name}说{query_text}"
        role_history = f"{role_name}说{answer_text}"
        chat_history = you_history + '\n' + role_history

        # 检查是否开启对话摘要
        enable_summary = self.sysConfig.enable_summary
        history = {}
        if enable_summary:
            memory_summary = MemorySummary(self.sysConfig)
            summary = memory_summary.summary(
                llm_model_type=self.sysConfig.summary_llm_model_driver_type, input=chat_history)
            history = {
                "summary": summary["summary"]
            }
        else:
            history = {
                "summary": chat_history
            }

        history_json = json.dumps(history)
        self.strategy.save(pk, history_json, you_name)

    def format_history(you_name: str, query_text: str, role_name: str, answer_text: str):
        you_history = f"{you_name}说{query_text}"
        role_history = f"{role_name}说{answer_text}"
        chat_history = you_history + '\n' + role_history
        return chat_history

    def get_current_entity_id(self) -> int:
        '''生成唯一标识'''
        return self.snow_flake.task()

    def clear(self, owner: str) -> None:
        return self.strategy.clear(owner)


class MemorySummary():

    sysConfig: SysConfig
    prompt: str

    def __init__(self, sysConfig: SysConfig) -> None:
        self.sysConfig = sysConfig
        self.prompt = '''
               <s>[INST] <<SYS>>          
                请帮我提取对话内容的关键信息，下面是一个提取关键信息的示例:
                ```
                input:"alan：你好，爱莉，很高兴认识你，我是一名程序员，我喜欢吃川菜，也喜欢打篮球，我是水瓶座，生日是1月29日
                output:{"summary"："alan向爱莉表示自己是一名程序员，爱莉表达对程序员的兴趣并希望了解更多","information":["alan是一名程序员","alan喜欢川菜","alan喜欢打篮球","alan是水瓶座","alan的生日是1月29日"]}
                ```
                输出格式请使用以下方式：
                ```
                {"summary":"对话摘要"}
                ```
                <</SYS>>
        '''

    def summary(self, llm_model_type: str, input: str) -> str:
        prompt = self.prompt + f"input:{input} [/INST]"
        result = self.sysConfig.llm_model_driver.chat(prompt=prompt, type=llm_model_type, role_name="",
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
