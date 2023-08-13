import re
from typing import Tuple
from ...llms.llm_model_strategy import LlmModelDriver
import numpy as np
from typing import List
from langchain.memory import ConversationBufferWindowMemory
from .milvus_storage_impl import MilvusStorage
from .local_storage_impl import LocalStorage
from .base_storage import BaseStorage
from ...utils.snowflake_utils import SnowFlake


class MemoryStorageDriver():

    strategy: BaseStorage
    short_memory_dict: dict[str, ConversationBufferWindowMemory] = {}
    tmp_k_num: int = 3
    snow_flake: SnowFlake = SnowFlake(data_center_id=5, worker_id=5)

    def __init__(self, type: str, memory_storage_config: dict[str, str]) -> None:
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
            short_memory_item = short_memory_dict.load_memory_variables({})[
                "history"]
            short_memory.append(short_memory_item)
        if len(short_memory) > 0:
            short_history = "\n".join(short_memory)

        # 获取长期记忆
        long_memory = self.strategy.search(
            query_text, 30, f"owner == '{owner}'")
        long_history = "[]"
        if len(long_memory) > 0:
            long_history = "\n".join(long_memory)

        return (short_history, long_history)

    def pageQuery(self, page_num: int, page_size: int, expr: str) -> list[str]:
        '''分页检索记忆'''
        return self.strategy.pageQuery(page_num=page_num, page_size=page_size, expr=expr)

    def save(self, role_name: str, you_name: str, query_text: str, answer_text: str, llm_model_type: str, llm_model_driver: LlmModelDriver) -> None:

        pk = self.get_current_entity_id()

        # 获取短期记忆存储对象，如果没有创建新的
        short_memory_dict = self.short_memory_dict.get(you_name, None)
        if short_memory_dict == None:
            new_short_memory_dict = ConversationBufferWindowMemory(
                k=self.tmp_k_num, human_prefix=you_name, ai_prefix=role_name)
            self.short_memory_dict[you_name] = new_short_memory_dict
            short_memory_dict = new_short_memory_dict

        short_memory_dict.save_context({"input": query_text}, {
            "output": answer_text})

        # 将当前对话语句生成摘要，存储为长期记忆
        you_history = f"{you_name}：{query_text}"
        role_history = f"{role_name}：{answer_text}"
        history = you_history + '\n' + role_history
        memory_summary = MemorySummary(llm_model_driver)
        history = memory_summary.summary(
            llm_model_type=llm_model_type, input=history)
        self.strategy.save(pk, history, you_name)

    def get_current_entity_id(self) -> int:
        '''生成唯一标识'''
        return self.snow_flake.task()

    def clear(self, owner: str) -> None:
        return self.strategy.clear(owner)


class MemorySummary():

    llm_model_driver: LlmModelDriver
    prompt: str

    def __init__(self, llm_model_driver: LlmModelDriver) -> None:
        self.llm_model_driver = llm_model_driver
        self.prompt = '''
          <s>[INST] <<SYS>>
          So to summarize the conversation I provided, just briefly describe what they did. and output it in the 
          "summary": "you summary"
          <</SYS>>
          {input} [/INST]
        '''

    def summary(self, llm_model_type: str, input: str) -> str:
        result = self.llm_model_driver.chat(prompt=self.prompt, type=llm_model_type, role_name="",
                                            you_name="", query=input, short_history="", long_history="")
        pattern = r'[Ss]ummary:\s*(.*)'
        match = re.search(pattern, result)

        if match:
            result = match.group(1)
        print("summary:", result)
        return result

# from typing import Any, Dict, List

# from langchain.memory.chat_memory import BaseChatMemory
# from langchain.schema import BaseMessage, get_buffer_string


# class VwConversationBufferWindowMemory(BaseChatMemory):
#     """Buffer for storing conversation memory."""

#     human_prefix: str = "Human"
#     ai_prefix: str = "AI"
#     memory_key: str = "history"  #: :meta private:
#     k: int = 5

#     @property
#     def buffer(self) -> List[BaseMessage]:
#         """String buffer of memory."""
#         return self.chat_memory.messages

#     @property
#     def memory_variables(self) -> List[str]:
#         """Will always return list of memory variables.

#         :meta private:
#         """
#         return [self.memory_key]

#     def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, str]:
#         """Return history buffer."""

#         buffer: Any = self.buffer[-self.k * 2 :] if self.k > 0 else []
#         if not self.return_messages:
#             buffer = get_buffer_string(
#                 buffer,
#                 human_prefix=self.human_prefix,
#                 ai_prefix=self.ai_prefix,
#             )
#         return {self.memory_key: buffer}

# class VwChatMessageHistory(BaseChatMessageHistory, BaseModel):

#     messages: List[BaseMessage] = []

#     def add_user_message(self, message: str) -> None:
#         self.messages.append(HumanMessage(content=message))

#     def add_ai_message(self, message: str) -> None:
#         self.messages.append(AIMessage(content=message))

#     def clear(self) -> None:
#         self.messages = []
