from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature=0.8,model_name="gpt-3.5-turbo")

class OpenAIGeneration():

    def chat(prompt: str, role_name: str, you_name: str, query: str, short_history: str, long_history: str) -> str:
        role_prompt_str = prompt.format(role_name=role_name,
                                        you_name=you_name, input="{input}", short_history=short_history, long_history=long_history)
        prompt = PromptTemplate(
            input_variables=["input"], template=role_prompt_str, validate_template=False
        )
        llm_chain = LLMChain(
            llm=llm,
            prompt=prompt,
            verbose=True
        )
        return llm_chain.predict(input=query)
