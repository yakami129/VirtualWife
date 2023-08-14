
from .base_custom_role_template import BaseCustomRoleTemplate
from .custom_role_model import CustomRoleModel


PROMPT = """
<s>[INST] <<SYS>>
{persona}
{scenario}
{role_name}的对话风格如下:
{examples_of_dialogue}
你扮演的是{role_name}，只站在{role_name}角度，输出{role_name}的对话。
你的回答应该简短，最多包含三句话，每句话不超过40个单词。
[这个是{role_name}的性格简述：{personality} 下面是 {you_name}和{role_name}的对话历史]：
{short_history}
[这个是{role_name}最近的回忆，你可以根据回忆，对{you_name}做出不同的反馈，比如讽刺、幽默、开玩笑、鼓励等反馈]：
{long_history}
<</SYS>>
{you_name}：{input}[/INST]
"""

PERSONALITY_PROMPT = "{role_name}'s personality: {personality}"

SCENARIO_PROMPT = "Circumstances and context of the dialogue: {scenario}"


class ChineseCustomRoleTemplate(BaseCustomRoleTemplate):

    def format(self, custom_role_model: CustomRoleModel) -> str:

        # 获取prompt参数
        role_name = custom_role_model.role_name
        persona = custom_role_model.persona
        examples_of_dialogue = custom_role_model.examples_of_dialogue
        you_name = "{you_name}"
        long_history = "{long_history}"
        short_history = "{short_history}"
        input = "{input}"

        # 格式化性格简述
        personality = custom_role_model.personality
        if personality != None and personality != '':
            personality = PERSONALITY_PROMPT.format(
                role_name=role_name, personality=personality)
        else:
            personality = ""

        # 格式化情景简述
        scenario = custom_role_model.scenario
        if scenario != None and scenario != '':
            scenario = SCENARIO_PROMPT.format(scenario=scenario)
        else:
            scenario = ""

        # Generate the prompt to be sent to the language model
        prompt = PROMPT.format(
            role_name=role_name, persona=persona, personality=personality,
            scenario=scenario, examples_of_dialogue=examples_of_dialogue, you_name=you_name,
            long_history=long_history, short_history=short_history, input=input
        )

        return prompt
