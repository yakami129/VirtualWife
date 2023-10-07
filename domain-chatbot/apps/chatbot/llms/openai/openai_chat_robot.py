import os
from ...utils.str_utils import remove_spaces_and_tabs
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
)
import openai


class OpenAIGeneration:
    llm: ChatOpenAI

    def __init__(self) -> None:
        from dotenv import load_dotenv
        load_dotenv()
        OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
        OPENAI_BASE_URL = os.environ['OPENAI_BASE_URL']
        if OPENAI_BASE_URL is not None and OPENAI_BASE_URL != "":
            self.llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo",
                                  openai_api_key=OPENAI_API_KEY, openai_api_base=OPENAI_BASE_URL)
        else:
            self.llm = ChatOpenAI(
                temperature=0.7, model_name="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)

    def chat(self, prompt: str, role_name: str, you_name: str, query: str, short_history: list[dict[str, str]],
             long_history: str) -> str:
        prompt = prompt + query
        print(f"prompt:{prompt}")
        llm_result = self.llm.generate(
            messages=[[HumanMessage(content=prompt)]])
        llm_result_text = llm_result.generations[0][0].text
        return llm_result_text

    async def chatStream(self,
                         prompt: str,
                         role_name: str,
                         you_name: str,
                         query: str,
                         history: list[dict[str, str]],
                         realtime_callback=None,
                         conversation_end_callback=None):
        messages = []
        for item in history:
            message = {"role": "user", "content": item["human"]}
            messages.append(message)
            message = {"role": "assistant", "content": item["ai"]}
            messages.append(message)
        messages.append({'role': 'system', 'content': prompt})
        messages.append({'role': 'user', 'content': you_name + "说" + query})
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=0,
            stream=True  # again, we set stream=True
        )
        # create variables to collect the stream of chunks
        answer = ''
        for part in response:
            finish_reason = part["choices"][0]["finish_reason"]
            if finish_reason is None and "delta" in part["choices"][0] and "content" in part["choices"][0]["delta"]:
                content = part["choices"][0]["delta"]["content"]
                # 过滤空格和制表符
                content = remove_spaces_and_tabs(content)
                if content == "":
                    continue
                answer += content
                if realtime_callback:
                    realtime_callback(role_name, you_name,
                                      content)  # 调用实时消息推送的回调函数
            elif finish_reason:
                if conversation_end_callback:
                    conversation_end_callback(role_name, answer, you_name,
                                              query)  # 调用对话结束消息的回调函数
                break  # 停止循环，对话已经结束
