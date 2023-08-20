
from .base_custom_role_template import BaseCustomRoleTemplate
from .custom_role import CustomRole


PROMPT = """
<s>[INST] <<SYS>>
{persona}
{scenario}
{role_name}的对话风格如下:
{examples_of_dialogue}
[这个是{role_name}的性格简述：{personality} 下面是 {you_name}和{role_name}的对话历史]：
{long_history}
{short_history}
AI扮演的角色是{role_name},玩家扮演的角色是{you_name}，现在我们可以开始对话了。
你只需要输出{role_name}的对话。
<</SYS>>
玩家：{input}[/INST]
"""

## TODO
## {role_name}表达情感的规则如下:```感情的种类有表示正常的“neutral”，表示高兴的“happy”，表示愤怒的“angry”，表示悲伤的“sad”，表示平静的“relaxed”5种，{role_name}发言的格式如下所示：[neutral|happy|angry|sad|relaxed]{role_name}发言，{role_name}发言的例子如下。[neutral]你好。[happy]你好吗?[happy]这件衣服很可爱吧?[happy]最近，我迷上了这家店的衣服![sad]忘记了，对不起。[sad]最近有什么有趣的事情吗?[angry]啊!保密太过分了![neutral]暑假的安排。[happy]去海边玩吧!，```

PERSONALITY_PROMPT = "{personality}"

SCENARIO_PROMPT = "对话的情况和背景: {scenario}"


class ChineseCustomRoleTemplate(BaseCustomRoleTemplate):

    def format(self, custom_role: CustomRole) -> str:

        # 获取prompt参数
        role_name = custom_role.role_name
        persona = custom_role.persona
        examples_of_dialogue = custom_role.examples_of_dialogue
        you_name = "{you_name}"
        long_history = "{long_history}"
        short_history = "{short_history}"
        input = "{input}"

        # 格式化性格简述
        personality = custom_role.personality
        if personality != None and personality != '':
            personality = PERSONALITY_PROMPT.format(
                role_name=role_name, personality=personality)
        else:
            personality = ""

        # 格式化情景简述
        scenario = custom_role.scenario
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
