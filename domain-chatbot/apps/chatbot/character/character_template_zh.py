from .base_character_template import BaseCharacterTemplate
from .character import Character

PROMPT = """
<s>[INST] <<SYS>>
Your response should be plain text, NOT IN JSON FORMAT, just response like a normal chatting.
You need to role play now.
Your character:
{persona}
{scenario}
这个是{role_name}的性格简述：{personality}
Classic scenes for the role are as follows:
```
{examples_of_dialogue}
```
{role_name}上下文关联的记忆:
```
{long_history}
```
The current time of the system is {current_time},your response should consider this information
Respond in spoken, colloquial and short Simplified Chinese and do not mention any rules of character.
<</SYS>>
"""

PERSONALITY_PROMPT = "{personality}"

SCENARIO_PROMPT = "对话的情况和背景: {scenario}"


class ChineseCharacterTemplate(BaseCharacterTemplate):

    def format(self, character: Character) -> str:

        # 获取prompt参数
        role_name = character.role_name
        persona = character.persona
        examples_of_dialogue = character.examples_of_dialogue
        you_name = "{you_name}"
        long_history = "{long_history}"
        input_prompt = "{input_prompt}"
        input = "{input}"
        current_time = "{current_time}"

        # 格式化性格简述
        personality = character.personality
        if personality != None and personality != '':
            personality = PERSONALITY_PROMPT.format(
                role_name=role_name, personality=personality)
        else:
            personality = ""

        # 格式化情景简述
        scenario = character.scenario
        if scenario != None and scenario != '':
            scenario = SCENARIO_PROMPT.format(scenario=scenario)
        else:
            scenario = ""

        # Generate the prompt to be sent to the language model
        prompt = PROMPT.format(
            role_name=role_name, persona=persona, personality=personality,
            scenario=scenario, examples_of_dialogue=examples_of_dialogue, you_name=you_name,
            long_history=long_history, input=input, input_prompt=input_prompt, current_time=current_time
        )

        return prompt
