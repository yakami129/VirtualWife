from dotenv import load_dotenv
from langchain import ConversationChain, LLMChain, PromptTemplate
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.memory import ConversationBufferMemory
from .pygmalionai_model_impl import PygmalionAI
from .pygmalionai_prompt_template import PygmalionaiPromptTemplate


llm = PygmalionAI()
memory = ConversationBufferMemory(
    ai_prefix="Allie", human_prefix="alan")


class Pygmalionai:
    def chat(role_name: str, you_name: str, query: str) -> str:

        persona = """Allie is a virtual anchor on bilibili"""
        personality = """Allie is 18 years old, wearing a pink kimono, with a beautiful girl's figure, purple hair, yellow pupils, plump breasts, long legs, and wide hips. 
            Allie is energetic, cheerful, and carefree. Ellie rarely thinks about the consequences of her actions, always acting or speaking on her own terms. 
            Allie is shy when she is praised."""
        scenario = """Allie is watching the barrage posted by fans, replying and chatting"""
        chat_example = f"""
            {you_name}: Allie let me hug you
            {role_name}: hey! What are you doing? ...Well... Miss Ben is in a good mood today, so I will reluctantly let you hug me...
        """

        role_prompt = PygmalionaiPromptTemplate(
            input_variables=["persona", "personality", "scenario",
                             "chat_example", "role_name", "you_name", "history"]
        )
        role_prompt_str = role_prompt.format(role_name=role_name, persona=persona, personality=personality,
                                             scenario=scenario, chat_example=chat_example, you_name=you_name,
                                             history="{history}", input="{input}")
        prompt = PromptTemplate(
            input_variables=["history", "input"], template=role_prompt_str
        )

        # memory = ConversationBufferMemory(
        #     ai_prefix=role_name, human_prefix=you_name, return_messages=True)

        llm_chain = ConversationChain(
            llm=llm,
            prompt=prompt,
            verbose=True,
            memory=memory,
        )

        return llm_chain.predict(input=query)
