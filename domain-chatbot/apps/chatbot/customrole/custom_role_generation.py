

from django.shortcuts import get_object_or_404
from ..models import CustomRoleModel
from .custom_role_template_en import EnglishCustomRoleTemplate
from .custom_role_template_zh import ChineseCustomRoleTemplate
from .base_custom_role_template import BaseCustomRoleTemplate
from .custom_role import CustomRole
from .sys.maiko_en import maiko_en
import json


class CustomRoleGeneration():

    custom_role_template_dict: dict[str, BaseCustomRoleTemplate] = {}

    def __init__(self) -> None:

        # 加载模型
        self.custom_role_template_dict["en"] = EnglishCustomRoleTemplate()
        self.custom_role_template_dict["zh"] = ChineseCustomRoleTemplate()

    def get_custom_role(self, role_id: int) -> CustomRole:
        '''获取角色定义对象'''
        custom_role = None
        custom_role_model = get_object_or_404(CustomRoleModel, pk=role_id)
        if custom_role_model == None:
            custom_role = maiko_en
        else:
            custom_role = CustomRole(
                role_name=custom_role_model.role_name,
                persona=custom_role_model.persona,
                personality=custom_role_model.personality,
                scenario=custom_role_model.scenario,
                examples_of_dialogue=custom_role_model.examples_of_dialogue,
                custom_role_template_type=custom_role_model.custom_role_template_type
            )
        return custom_role

    def output_prompt(self, custom_role: CustomRole) -> str:
        '''获取角色定义prompt'''
        custom_role_template = self.custom_role_template_dict[
            custom_role.custom_role_template_type]
        return custom_role_template.format(custom_role)


singleton_custom_role_generation = CustomRoleGeneration()
