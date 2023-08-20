from __future__ import annotations
from abc import ABC, abstractmethod
from .openai.openai_chat_robot import OpenAIGeneration
from .text_generation.text_generation_chat_robot import TextGeneration


class LlmModelStrategy(ABC):
    @abstractmethod
    def chat(self, prompt: str, role_name: str, you_name: str, query: str, short_history: str, long_history: str) -> str:
        pass


# 定义策略类实现
class OpenAILlmModelStrategy(LlmModelStrategy):

    openai_generation: OpenAIGeneration

    def __init__(self) -> None:
        super().__init__()
        self.openai_generation = OpenAIGeneration()

    def chat(self, prompt: str, role_name: str, you_name: str, query: str, short_history: str, long_history: str) -> str:
        return self.openai_generation.chat(prompt=prompt, role_name=role_name, you_name=you_name, query=query, short_history=short_history, long_history=long_history)


class TextGenerationLlmModelStrategy(LlmModelStrategy):

    generation : TextGeneration

    def __init__(self) -> None:
        super().__init__()
        self.generation = TextGeneration()

    def chat(self, prompt: str, role_name: str, you_name: str, query: str, short_history: str, long_history: str) -> str:
        return self.generation.chat(prompt=prompt, role_name=role_name, you_name=you_name, query=query, short_history=short_history, long_history=long_history)


# 定义驱动类
class LlmModel:
    def __init__(self, strategy: LlmModelStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: LlmModelStrategy) -> None:
        self._strategy = strategy

    def chat(self, prompt: str, role_name: str, you_name: str, query: str, short_history: str, long_history: str) -> str:
        return self._strategy.chat(prompt=prompt, role_name=role_name, you_name=you_name, query=query, short_history=short_history, long_history=long_history)


class LlmModelDriver():

    openai: OpenAILlmModelStrategy
    textGeneration: TextGenerationLlmModelStrategy

    def __init__(self) -> None:
        self.openai = OpenAIGeneration()
        self.textGeneration = TextGenerationLlmModelStrategy()

    def chat(self, prompt: str, type: str, role_name: str, you_name: str, query: str, short_history: str, long_history: str) -> str:
        if type == "openai":
            strategy = self.openai
        elif type == "text_generation":
            strategy = self.textGeneration
        else:
            raise ValueError("Unknown type")

        llmModel = LlmModel(strategy)
        result = llmModel.chat(prompt=prompt, role_name=role_name,
                               you_name=you_name, query=query, short_history=short_history, long_history=long_history)

        return result
