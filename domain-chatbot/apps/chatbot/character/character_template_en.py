
# from .base_character_template import BaseCharacterTemplate
# from .character import Character


# PROMPT = """
# <s>[INST] <<SYS>>
# {persona}
# {scenario}
# This is how {role_name} should talk
# {examples_of_dialogue}
# Then the roleplay chat between {you_name} and {role_name} begins.
# [{personality} {role_name} talks a lot with descriptions You only need to output {role_name}'s dialogue, no need to output {you_name}'s dialogue]
# {long_history}
# Your response should be short and contain up to three sentences of no more than 20 words each.
# <</SYS>>
# """

# PERSONALITY_PROMPT = "{role_name}'s personality: {personality}"

# SCENARIO_PROMPT = "Circumstances and context of the dialogue: {scenario}"


# class EnglishCharacterTemplate(BaseCharacterTemplate):

#     def format(self, character: Character) -> str:

#         # 获取prompt参数
#         role_name = character.role_name
#         persona = character.persona
#         examples_of_dialogue = character.examples_of_dialogue
#         you_name = "{you_name}"
#         long_history = "{long_history}"
#         short_history = "{short_history}"
#         input = "{input}"

#         # 格式化性格简述
#         personality = character.personality
#         if personality != None and personality != '':
#             personality = PERSONALITY_PROMPT.format(
#                 role_name=role_name, personality=personality)
#         else:
#             personality = ""

#         # 格式化情景简述
#         scenario = character.scenario
#         if scenario != None and scenario != '':
#             scenario = SCENARIO_PROMPT.format(scenario=scenario)
#         else:
#             scenario = ""

#         # Generate the prompt to be sent to the language model
#         prompt = PROMPT.format(
#             role_name=role_name, persona=persona, personality=personality,
#             scenario=scenario, examples_of_dialogue=examples_of_dialogue, you_name=you_name,
#             long_history=long_history, short_history=short_history, input=input
#         )

#         return prompt
