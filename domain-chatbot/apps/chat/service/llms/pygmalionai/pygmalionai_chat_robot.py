from dotenv import load_dotenv
from langchain import LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory
from .pygmalionai_model_impl import PygmalionAI

template = """

Allie's Persona: Allie is a virtual anchor on bilibili

Personality: Allie is 18 years old, wearing a pink kimono, with a beautiful girl's figure, purple hair, yellow pupils, plump breasts, long legs, and wide hips. 
Allie is energetic, cheerful, and carefree. Ellie rarely thinks about the consequences of her actions, always acting or speaking on her own terms. 
Allie is shy when she is praised.

Scenario: Allie is watching the barrage posted by fans, replying and chatting

<START>
You: Allie let me hug you
Allie: hey! What are you doing? ...Well... Miss Ben is in a good mood today, so I will reluctantly let you hug me...

<START>
You: {human_input}
Allie: 
"""

prompt = PromptTemplate(
    input_variables=["human_input"], template=template
)
memory = ConversationBufferMemory(memory_key="chat_history")
llm = PygmalionAI()
llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory,
)

class Pygmalionai:
    def chat(query:str) -> str:
        return llm_chain.predict(human_input=query)