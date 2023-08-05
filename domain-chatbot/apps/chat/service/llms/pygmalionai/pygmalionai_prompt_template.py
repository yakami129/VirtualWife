from langchain.prompts import StringPromptTemplate
from pydantic import BaseModel, validator

PROMPT = """
{role_name}'s Persona: {persona}

Personality: {personality}

Scenario: {scenario}

<START>
{chat_example}

<START>
{history}

<START>
{you_name}: {input}
{role_name}: 
"""


class PygmalionaiPromptTemplate(StringPromptTemplate, BaseModel):
    """"""

    @validator("input_variables")
    def validate_input_variables(cls, v):
        """Validate that the input variables are correct."""
        return v

    def format(self, **kwargs) -> str:

        # 获取prompt参数
        role_name = kwargs["role_name"]
        persona = kwargs["persona"]
        personality = kwargs["personality"]
        scenario = kwargs["scenario"]
        chat_example = kwargs["chat_example"]
        you_name = kwargs["you_name"]
        history = kwargs["history"]
        input = kwargs["input"]

        # Generate the prompt to be sent to the language model
        prompt = PROMPT.format(
            role_name=role_name, persona=persona, personality=personality,
            scenario=scenario, chat_example=chat_example, you_name=you_name,
            history=history, input=input

        )
        return prompt

    def _prompt_type(self):
        return "function-explainer"
