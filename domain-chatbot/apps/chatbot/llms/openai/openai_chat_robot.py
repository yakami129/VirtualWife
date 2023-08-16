from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
)
import logging

llm = ChatOpenAI(temperature=0.9,model_name="gpt-3.5-turbo")

class OpenAIGeneration():

    def chat(prompt: str, role_name: str, you_name: str, query: str, short_history: str, long_history: str) -> str:
        logging.info(f"prompt:{prompt}")
        llm_result = llm.generate(messages=[[HumanMessage(content=prompt)]])
        llm_result_text = llm_result.generations[0][0].text
        return llm_result_text;