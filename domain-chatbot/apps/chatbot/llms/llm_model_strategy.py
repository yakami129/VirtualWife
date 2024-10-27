from __future__ import annotations
from abc import ABC, abstractmethod
import threading
import asyncio
from typing import List, Dict

from .ollama.ollama_chat_robot import OllamaGeneration
from .openai.openai_chat_robot import OpenAIGeneration
from .zhipuai.zhipuai_chat_robot import ZhipuAIGeneration
from ..memory.zep.zep_memory import ChatHistroy


class LlmModelStrategy(ABC):

    @abstractmethod
    def chat(self, prompt: str, role_name: str, you_name: str, query: str, short_history: list[ChatHistroy],
             long_history: str) -> str:
        pass

    @abstractmethod
    async def chatStream(self,
                         prompt: str,
                         role_name: str,
                         you_name: str,
                         query: str,
                         history: list[ChatHistroy],
                         realtime_callback=None,
                         conversation_end_callback=None):
        pass


# 定义策略类实现
class OpenAILlmModelStrategy(LlmModelStrategy):
    openai_generation: OpenAIGeneration

    def __init__(self) -> None:
        super().__init__()
        self.openai_generation = OpenAIGeneration()

    def chat(self, prompt: str, role_name: str, you_name: str, query: str, short_history: list[ChatHistroy],
             long_history: str) -> str:
        return self.openai_generation.chat(prompt=prompt, role_name=role_name, you_name=you_name, query=query,
                                           short_history=short_history, long_history=long_history)

    async def chatStream(self,
                         prompt: str,
                         role_name: str,
                         you_name: str,
                         query: str,
                         history: list[ChatHistroy],
                         realtime_callback=None,
                         conversation_end_callback=None
                         ):
        return await self.openai_generation.chatStream(prompt=prompt,
                                                       role_name=role_name,
                                                       you_name=you_name,
                                                       query=query,
                                                       history=history,
                                                       realtime_callback=realtime_callback,
                                                       conversation_end_callback=conversation_end_callback)


class OllamaLlmModelStrategy(LlmModelStrategy):
    ollama_generation: OllamaGeneration

    def __init__(self) -> None:
        super().__init__()
        self.ollama_generation = OllamaGeneration()

    def chat(self, prompt: str, role_name: str, you_name: str, query: str, short_history: list[ChatHistroy],
             long_history: str) -> str:
        return self.ollama_generation.chat(prompt=prompt, role_name=role_name, you_name=you_name, query=query,
                                           short_history=short_history, long_history=long_history)

    async def chatStream(self,
                         prompt: str,
                         role_name: str,
                         you_name: str,
                         query: str,
                         history: list[ChatHistroy],
                         realtime_callback=None,
                         conversation_end_callback=None
                         ):
        return await self.ollama_generation.chatStream(prompt=prompt,
                                                       role_name=role_name,
                                                       you_name=you_name,
                                                       query=query,
                                                       history=history,
                                                       realtime_callback=realtime_callback,
                                                       conversation_end_callback=conversation_end_callback)

class ZhipuaiLlmModelStrategy(LlmModelStrategy):
    def __init__(self):
        self.zhipuai = ZhipuAIGeneration()  # 确保已经有了ZhipuAIGeneration类的实现

    def chat(self, prompt: str, role_name: str, you_name: str, query: str,
             short_history: List[ChatHistroy], long_history: str) -> str:
        # 这里简化了实现，具体实现应该根据ZhipuAIGeneration的chat方法来
        return self.zhipuai.chat(prompt, role_name, you_name, query, short_history, long_history)

    async def chatStream(self, prompt: str, role_name: str, you_name: str, query: str,
                         history: List[Dict[str, str]], realtime_callback=None, conversation_end_callback=None):
        # 这里简化了实现，具体实现应该根据ZhipuAIGeneration的chatStream方法来
        await self.zhipuai.chatStream(prompt, role_name, you_name, query, history, realtime_callback, conversation_end_callback)


class LlmModelDriver:

    def __init__(self):
        self.openai = OpenAIGeneration()
        self.ollama = OllamaLlmModelStrategy()
        self.zhipuai = ZhipuaiLlmModelStrategy()
        self.chat_stream_lock = threading.Lock()

    def chat(self, prompt: str, type: str, role_name: str, you_name: str, query: str,
             short_history: list[ChatHistroy], long_history: str) -> str:
        strategy = self.get_strategy(type)
        result = strategy.chat(prompt=prompt, role_name=role_name,
                               you_name=you_name, query=query, short_history=short_history, long_history=long_history)
        return result

    def chatStream(self,
                   prompt: str,
                   type: str,
                   role_name: str,
                   you_name: str,
                   query: str,
                   history: list[ChatHistroy],
                   realtime_callback=None,
                   conversation_end_callback=None):
        strategy = self.get_strategy(type)
        asyncio.run(strategy.chatStream(prompt=prompt,
                                        role_name=role_name,
                                        you_name=you_name,
                                        query=query,
                                        history=history,
                                        realtime_callback=realtime_callback,
                                        conversation_end_callback=conversation_end_callback))

    def get_strategy(self, type: str) -> LlmModelStrategy:
        if type == "openai":
            return self.openai
        elif type == "ollama":
            return self.ollama
        elif type == "zhipuai":
            return self.zhipuai
        else:
            raise ValueError("Unknown type")
