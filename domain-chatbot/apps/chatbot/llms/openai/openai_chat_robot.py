import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
)
import logging


class OpenAIGeneration():

    llm: ChatOpenAI

    def __init__(self) -> None:
        from dotenv import load_dotenv
        load_dotenv() 
        OPENAI_API_KEY = os.environ['OPENAI_API_KEY'] 
        OPENAI_BASE_URL = os.environ['OPENAI_BASE_URL']
        if OPENAI_BASE_URL != None and OPENAI_BASE_URL != "":
            self.llm = ChatOpenAI(temperature=0.9,model_name="gpt-3.5-turbo",openai_api_key=OPENAI_API_KEY,openai_api_base=OPENAI_BASE_URL)
        else:
            self.llm = ChatOpenAI(temperature=0.9,model_name="gpt-3.5-turbo",openai_api_key=OPENAI_API_KEY)
           
    def chat(self,prompt: str, role_name: str, you_name: str, query: str, short_history: str, long_history: str) -> str:
        print(f"prompt:{prompt}")
        llm_result = self.llm.generate(messages=[[HumanMessage(content=prompt)]])
        llm_result_text = llm_result.generations[0][0].text
        return llm_result_text;