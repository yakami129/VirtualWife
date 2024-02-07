class Character():
    '''统一自定义角色定义数据结构

    role_name: 角色名称
    persona: 角色基本信息定义
    personality: 角色的性格简短描述
    scenario: 角色的对话的情况和背景
    examples_of_dialogue: 角色的对话样例

    '''
    role_name: str
    persona: str
    personality: str
    scenario: str
    examples_of_dialogue: str
    custom_role_template_type: str
    role_package_id: int

    def __init__(self, role_name: str, persona: str, personality: str, scenario: str, examples_of_dialogue,
                 custom_role_template_type: str, role_package_id: int) -> None:
        self.role_name = role_name
        self.persona = persona
        self.personality = personality
        self.scenario = scenario
        self.examples_of_dialogue = examples_of_dialogue
        self.custom_role_template_type = custom_role_template_type
        self.role_package_id = role_package_id

    def to_dict(self):
        return {
            "role_name": self.role_name,
            "persona": self.persona,
            "personality": self.personality,
            "scenario": self.scenario,
            "examples_of_dialogue": self.examples_of_dialogue,
            "custom_role_template_type": self.custom_role_template_type,
            "role_package_id": self.role_package_id
        }
