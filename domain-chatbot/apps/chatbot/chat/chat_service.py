
from ..customrole.custom_role_generation import CustomRoleGeneration
from ..memory.storage.memory_storage_strategy import MemoryStorageDriver
from ..llms.llm_model_strategy import LlmModelDriver
import logging
import re


class ChatService():

    llm_model_driver: LlmModelDriver
    llm_model_type: str
    memory_storage_driver: MemoryStorageDriver
    memory_storage_config: dict[str, str]
    memory_type: str
    custom_role_generation: CustomRoleGeneration

    def __init__(self) -> None:

        # 加载记忆模块配置
        self.memory_type = 'milvus'
        self.memory_storage_config = {
            "host": "127.0.0.1",
            "port": "19530",
            "user": "root",
            "password": "Milvus",
            "db_name": "default"
        }

        # 加载记忆模块驱动
        self.memory_storage_driver = MemoryStorageDriver(
            type=self.memory_type, memory_storage_config=self.memory_storage_config)

        # 加载自定义角色生成模块
        self.custom_role_generation = CustomRoleGeneration()

        # 加载聊天模型
        self.llm_model_driver = LlmModelDriver()
        self.llm_model_type = "pygmalionai"

    def chat(self, role_name: str, you_name: str, query: str) -> str:

        # 生成角色prompt
        prompt = self.custom_role_generation.get_prompt(role_name)

        # 检索相关记忆
        history_arr = self.memory_storage_driver.search(
            query_text=query, owner=you_name)
        history = ""
        if len(history_arr) > 0:
            history = "\n".join(history_arr)

        # 对话聊天
        answer_text = self.llm_model_driver.chat(prompt=prompt, type=self.llm_model_type, role_name=role_name,
                                                 you_name=you_name, query=query, history=history)
        answer_text = self.format_chat_text(
            role_name=role_name, you_name=you_name, text=answer_text)

        # 保存记忆
        self.memory_storage_driver.save(
            role_name=role_name, you_name=you_name, query_text=query, answer_text=answer_text)

        logging.info(
            f'[BIZ] # ChatService.chat # role_name：{role_name} you_name：{you_name} query：{query} history：{history} # \n => answer_text：{answer_text}')

        # self.memory_storage_driver.clear(owner=you_name)

        # 合成语音
        return answer_text

    def format_chat_text(self, role_name: str, you_name: str, text: str):
        # 去除特殊字符 * 、`role_name：`、`you_name:`
        text = text.replace(f'*', "")
        text = text.replace(f'{role_name}：', "")
        text = text.replace(f'{you_name}：', "")
        text = text.replace(f'{role_name}:', "")
        text = text.replace(f'{you_name}:', "")
        return text
