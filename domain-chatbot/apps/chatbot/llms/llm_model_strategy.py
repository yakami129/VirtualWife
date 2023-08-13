from __future__ import annotations
from abc import ABC, abstractmethod
# from .openai.aili_anchor_chat_robot import Aili
# from .openai.cat_lady_chat_robot import CatLady
# from .openai.enice_chat_robot import Enice
from .text_generation.text_generation_chat_robot import TextGeneration
# 定义llm_model的抽象类


class LlmModelStrategy(ABC):
    @abstractmethod
    def chat(self, prompt: str, role_name: str, you_name: str, query: str, short_history: str, long_history: str) -> str:
        pass


# 定义策略类实现
class OpenAILlmModelStrategy(LlmModelStrategy):
    def chat(self, prompt: str, role_name: str, you_name: str, query: str, short_history: str, long_history: str) -> str:
        result = ""
        # if role_name == "aili":
        #     result = Aili.chat(query=query)
        # elif role_name == "catLady":
        #     result = CatLady.chat(query=query)
        # elif role_name == 'enice':
        #     result = Enice.chat(query=query)
        return result


class TextGenerationLlmModelStrategy(LlmModelStrategy):
    def chat(self, prompt: str, role_name: str, you_name: str, query: str, short_history: str, long_history: str) -> str:
        return TextGeneration.chat(prompt=prompt, role_name=role_name, you_name=you_name, query=query, short_history=short_history, long_history=long_history)


# 定义驱动类
class LlmModel:
    def __init__(self, strategy: LlmModelStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: LlmModelStrategy) -> None:
        self._strategy = strategy

    def chat(self, prompt: str, role_name: str, you_name: str, query: str, short_history: str, long_history: str) -> str:
        return self._strategy.chat(prompt=prompt, role_name=role_name, you_name=you_name, query=query, short_history=short_history, long_history=long_history)


class LlmModelDriver():

    def chat(self, prompt: str, type: str, role_name: str, you_name: str, query: str, short_history: str, long_history: str) -> str:
        if type == "openai":
            strategy = OpenAILlmModelStrategy()
        elif type == "pygmalionai":
            strategy = TextGenerationLlmModelStrategy()
        else:
            raise ValueError("Unknown type")

        llmModel = LlmModel(strategy)
        result = llmModel.chat(prompt=prompt, role_name=role_name,
                               you_name=you_name, query=query, short_history=short_history, long_history=long_history)

        return result
