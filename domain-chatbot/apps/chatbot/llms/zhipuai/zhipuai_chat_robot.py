import logging
import os

from zhipuai import ZhipuAI

from ...utils.chat_message_utils import format_chat_text
from ...utils.str_utils import remove_spaces_and_tabs
from ...memory.zep.zep_memory import ChatHistroy

logger = logging.getLogger(__name__)


class ZhipuAIGeneration:
    model_name: str = "glm-4"
    temperature: float = 0.7
    zhipuai_api_key: str

    def __init__(self) -> None:
        from dotenv import load_dotenv
        load_dotenv()
        self.zhipuai_api_key = os.environ['ZHIPUAI_API_KEY']
        self.client = ZhipuAI(api_key=self.zhipuai_api_key)

    def chat(self, prompt: str, role_name: str, you_name: str, query: str, short_history: list[ChatHistroy],
             long_history: str) -> str:
        prompt = prompt + query
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            stream=False,
            temperature=self.temperature,
        )

        llm_result_text = response.choices[0].message.content
        return llm_result_text

    async def chatStream(self, prompt: str, role_name: str, you_name: str, query: str, history: list[dict[str, str]],
                         realtime_callback=None, conversation_end_callback=None):

        messages = [{'role': 'system', 'content': prompt}]
        for item in history:
            messages.append({'role': 'user', 'content': item["human"]})
            messages.append({'role': 'assistant', 'content': item["ai"]})
        messages.append({'role': 'user', 'content': you_name + "说" + query})

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            stream=True,
            temperature=self.temperature,
        )

        answer = ''
        for chunk in response:
            print(f">>>> chunk {chunk}")
            if  len(chunk.choices) > 0:
                event_text = chunk.choices[0].delta.content
                print(f">>>> event_text {event_text}")
                if isinstance(event_text, str) and event_text != "":
                    content = remove_spaces_and_tabs(event_text)
                    if content == "":
                        continue
                    answer += content
                    if realtime_callback:
                        realtime_callback(role_name, you_name, content, False)

        answer = format_chat_text(role_name, you_name, answer)
        if conversation_end_callback:
            conversation_end_callback(role_name, answer, you_name, query)
