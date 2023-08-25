
from ..character.character_generation import singleton_character_generation
from ..config import singleton_sys_config
import logging
import re


# class ChatService():

#     def __init__(self) -> None:

#         # 加载自定义角色生成模块
#         self.singleton_character_generation = singleton_character_generation

#     def chat(self, you_name: str, query: str) -> str:

#         # 生成角色prompt
#         custom_role = self.singleton_character_generation.get_custom_role(
#             singleton_sys_config.character)
#         role_name = custom_role.role_name
#         prompt = self.singleton_character_generation.output_prompt(custom_role)

#         # 检索相关记忆
#         short_history, long_history = singleton_sys_config.memory_storage_driver.search(
#             query_text=query, you_name=you_name, role_name=role_name)

#         # 对话聊天
#         prompt = prompt.format(input=query, you_name=you_name,
#                                short_history=short_history, long_history=long_history)
#         answer_text = singleton_sys_config.llm_model_driver.chat(prompt=prompt, type=singleton_sys_config.conversation_llm_model_driver_type, role_name=role_name,
#                                                                  you_name=you_name, query=query, short_history=short_history, long_history=long_history)

#         # 格式化输出结果
#         answer_text = self.format_chat_text(
#             role_name=role_name, you_name=you_name, text=answer_text).strip()

#         logging.info(
#             f'[BIZ] # ChatService.chat # role_name：{role_name} you_name：{you_name} query：{query} short_history：{short_history}  long_history:{long_history}# \n => answer_text：{answer_text}')

#         if answer_text != "":
#             # 保存记忆
#             singleton_sys_config.memory_storage_driver.save(
#                 role_name=role_name, you_name=you_name, query_text=query, answer_text=answer_text)

#         return answer_text

#     def format_chat_text(self, role_name: str, you_name: str, text: str):
#         # 去除特殊字符 * 、`role_name：`、`you_name:`
#         # text = text.replace(f'*', "")
#         pattern = r'\*.*?\*'
#         text = text.replace(f'`', "")
#         text = re.sub(pattern, '', text)
#         text = text.replace(f'{role_name}：', "")
#         text = text.replace(f'{you_name}：', "")
#         text = text.replace(f'{role_name}:', "")
#         text = text.replace(f'{you_name}:', "")
#         text = text.replace(f'AI角色：', "")
#         text = text.replace(f'AI（{role_name}）：', "")
#         text = text.replace(f'AI：', "")
#         return text
