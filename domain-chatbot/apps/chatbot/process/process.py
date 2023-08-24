
from ..character.character_generation import singleton_character_generation
from ..config import singleton_sys_config
from ..output.realtime_message_queue import realtime_callback
import logging
import re


class ProcessCore():

    def __init__(self) -> None:

        # 加载自定义角色生成模块
        self.singleton_character_generation = singleton_character_generation

    def chat(self, you_name: str, query: str):

        # 生成角色prompt
        custom_role = self.singleton_character_generation.get_custom_role(
            singleton_sys_config.character)
        role_name = custom_role.role_name
        prompt = self.singleton_character_generation.output_prompt(custom_role)
        # TODO返回情绪值

        # 检索关联的短期记忆和长期记忆
        short_history, long_history = singleton_sys_config.memory_storage_driver.search(
            query_text=query, you_name=you_name, role_name=role_name)

        # 调用大语言模型流式生成对话
        prompt = prompt.format(input=query, you_name=you_name,
                               short_history=short_history, long_history=long_history)
        singleton_sys_config.llm_model_driver.chatStream(prompt=prompt,
                                                         type=singleton_sys_config.conversation_llm_model_driver_type,
                                                         role_name=role_name,
                                                         you_name=you_name,
                                                         query=query,
                                                         history=[],
                                                         realtime_callback=realtime_callback,
                                                         conversation_end_callback=conversation_end_callback)


def conversation_end_callback(role_name: str, you_name: str, query: str, content: str):
    print("对话已结束:", content)
