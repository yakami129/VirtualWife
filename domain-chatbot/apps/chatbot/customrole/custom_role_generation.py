

from .custom_role_template_en import EnglishCustomRoleTemplate
from .custom_role_template_zh import ChineseCustomRoleTemplate
from .base_custom_role_template import BaseCustomRoleTemplate
from .custom_role_model import CustomRoleModel
from .sys.maiko_en import maiko_en
from .sys.maiko_zh import maiko_zh


class CustomRoleGeneration():

    custom_role_model_dict: dict[str, CustomRoleModel] = {}
    custom_role_template_dict: dict[str, BaseCustomRoleTemplate] = {}

    def __init__(self) -> None:

        # 加载模型
        self.custom_role_template_dict["en"] = EnglishCustomRoleTemplate()
        self.custom_role_template_dict["zh"] = ChineseCustomRoleTemplate()

        # 加载系统内置角色
        self.custom_role_model_dict["爱莉"] = maiko_zh
        self.custom_role_model_dict["Maiko"] = maiko_en

        # TODO 加载用户自定义角色

    def list(self) -> list[str]:
        '''获取角色列表'''
        return self.custom_role_model_dict.keys()

    def get(self, role_name: str) -> CustomRoleModel:
        '''获取角色定义对象'''
        return self.custom_role_model_dict[role_name]

    def get_prompt(self, role_name: str) -> str:
        '''获取角色定义prompt'''
        custom_role_model = self.get(role_name)
        custom_role_template = self.custom_role_template_dict[
            custom_role_model.custom_role_template_type]
        return custom_role_template.format(custom_role_model)

singleton_custom_role_generation = CustomRoleGeneration()