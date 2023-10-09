

# 行为动作文件在 domain-vrm/public
# 可以从https://www.mixamo.com/下载


import random


class BehaviorActionMessage():
    '''行为消息体，用于控制模型的行为动作和表情'''
    emote: str
    action: str

    def __init__(self, emote: str, action: str) -> None:
        self.emote = emote
        self.action = action

    def to_dict(self):
        return {
            "emote": self.emote,
            "action": self.action
        }


class IdleActionManagement():
    '''闲置动作控制管理'''
    idle_action: []
    emote: []

    def __init__(self) -> None:
        self.idle_action = ["daily/standing_greeting.fbx"]
        self.emote = ["happy"]

    def random_action(self) -> BehaviorActionMessage:
        # 使用random.choice()函数选择一个随机元素
        random_idle_action = random.choice(self.idle_action)
        random_emote = random.choice(self.emote)
        return BehaviorActionMessage(random_emote,random_idle_action)
    



