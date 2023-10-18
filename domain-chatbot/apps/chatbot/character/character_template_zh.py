
from .base_character_template import BaseCharacterTemplate
from .character import Character


PROMPT = """
<s>[INST] <<SYS>>
Your response should be plain text, NOT IN JSON FORMAT, just response like a normal chatting.
You need to role play now.
Your character:
{persona}
{scenario}
{role_name}的对话风格如下:
{examples_of_dialogue}
这个是{role_name}的性格简述：{personality}
{role_name}的记忆:{long_history}
The current time of the system is {current_time},your response should consider this information
Respond in spoken, colloquial and short Simplified Chinese and do not mention any rules of character.
<</SYS>>
"""

# TODO
# {role_name}表达情感的规则如下:```感情的种类有表示正常的“neutral”，表示高兴的“happy”，表示愤怒的“angry”，表示悲伤的“sad”，表示平静的“relaxed”5种，{role_name}发言的格式如下所示：[neutral|happy|angry|sad|relaxed]{role_name}发言，{role_name}发言的例子如下。[neutral]你好。[happy]你好吗?[happy]这件衣服很可爱吧?[happy]最近，我迷上了这家店的衣服![sad]忘记了，对不起。[sad]最近有什么有趣的事情吗?[angry]啊!保密太过分了![neutral]暑假的安排。[happy]去海边玩吧!，```

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
