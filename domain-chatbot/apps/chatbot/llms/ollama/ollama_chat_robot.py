import logging
import os
from typing import List

from litellm import completion

from ...utils.chat_message_utils import format_chat_text
from ...utils.str_utils import remove_spaces_and_tabs
from ...memory.zep.zep_memory import ChatHistroy

logger = logging.getLogger(__name__)


class OllamaGeneration:
    model_name: str
    temperature: float = 0.7
    ollama_api_base: str

    def __init__(self) -> None:
        from dotenv import load_dotenv
        load_dotenv()
        self.ollama_api_base = os.environ['OLLAMA_API_BASE']
        self.model_name = "ollama/" + os.environ['OLLAMA_API_MODEL_NAME']

    def chat(self, prompt: str, role_name: str, you_name: str, query: str, short_history: list[ChatHistroy],
             long_history: str) -> str:
        prompt = prompt + query
        messages = [{"content": prompt, "role": "user"}]
        if self.ollama_api_base:
            response = completion(
                model=self.model_name,
                messages=messages,
                api_base=self.ollama_api_base,
                temperature=self.temperature,
            )
        else:
            response = completion(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
            )
        llm_result_text = response.choices[0].message.content if response.choices else ""
        return llm_result_text

    async def chatStream(self,
                         prompt: str,
                         role_name: str,
                         you_name: str,
                         query: str,
                         history: list[str, str],
                         realtime_callback=None,
                         conversation_end_callback=None):

        messages = []
        messages.append({'role': 'system', 'content': prompt})
        for item in history:
            message = {"role": "user", "content": item["human"]}
            messages.append(message)
            message = {"role": "assistant", "content": item["ai"]}
            messages.append(message)
        messages.append({'role': 'user', 'content': you_name + "说" + query})

        if self.ollama_api_base:
            response = completion(
                model=self.model_name,
                messages=messages,
                api_base=self.ollama_api_base,
                stream=True,
                temperature=self.temperature,
            )
        else:
            response = completion(
                model=self.model_name,
                messages=messages,
                stream=True,
                temperature=self.temperature,
            )

        answer = ''
        for event in response:
            if not isinstance(event, dict):
                event = event.model_dump()
            if isinstance(event['choices'], List) and len(event['choices']) > 0:
                event_text = event["choices"][0]['delta']['content']
                if isinstance(event_text, str) and event_text != "":
                    content = event_text
                    # 过滤空格和制表符
                    content = remove_spaces_and_tabs(content)
                    if content == "":
                        continue
                    answer += content
                    if realtime_callback:
                        realtime_callback(role_name, you_name,
                                          content, False)  # 调用实时消息推送的回调函数

        answer = format_chat_text(role_name, you_name, answer)
        if conversation_end_callback:
            realtime_callback(role_name, you_name, "", True)
            conversation_end_callback(role_name, answer, you_name, query)  # 调用对话结束消息的回调函数
