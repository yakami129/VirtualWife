from dotenv import load_dotenv
from langchain import LLMChain, PromptTemplate
from .text_generation_model_impl import TextGenerationModel

llm = TextGenerationModel()


class TextGeneration():

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
