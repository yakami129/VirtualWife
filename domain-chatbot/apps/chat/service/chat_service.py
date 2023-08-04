
from llms.llm_model_strategy import LlmModelDriver


class ChatService():

    def chat(self, type: str, role_name: str, query: str) -> str:

        # TODO敏感词过滤

        # 对话聊天
        llmModelDriver = LlmModelDriver()
        llmModelDriver.chat(type=type, role_name=role_name, query=query)

        # 合成语音

        return 


if __name__ == "__main__":
    chat_service = ChatService();
    result = chat_service.chat(type="pygmalionai",role_name="demo",query="你是谁？")