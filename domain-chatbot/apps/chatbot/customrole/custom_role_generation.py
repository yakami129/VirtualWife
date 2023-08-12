

from .custom_role_template import CustomRoleTemplate
from .custom_role_model import CustomRoleModel
from .sys.maiko import maiko


class CustomRoleGeneration():

    custom_role_model_dict: dict[str, CustomRoleModel] = {}

    def __init__(self) -> None:

        # 加载系统内置角色
        self.custom_role_model_dict["Maiko"] = maiko

        # TODO 加载用户自定义角色

    def list(self) -> list[str]:
        '''获取角色列表'''
        return self.custom_role_model_dict.keys()

    def get(self, role_name: str) -> str:
        '''获取角色定义对象'''
        return self.custom_role_model_dict[role_name]

    def get_prompt(self, role_name: str) -> str:
        '''获取角色定义prompt'''
        custom_role_model = self.get(role_name)
        custom_role_template = CustomRoleTemplate()
        return custom_role_template.format(custom_role_model)
