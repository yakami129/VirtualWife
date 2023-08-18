from django.db import models

# Create your models here.

class CustomRoleModel(models.Model):
    '''统一自定义角色定义数据结构

    role_name: 角色名称
    persona: 角色基本信息定义
    personality: 角色的性格简短描述
    scenario: 角色的对话的情况和背景
    examples_of_dialogue: 角色的对话样例

    '''
    role_name = models.CharField(max_length=100)
    persona = models.TextField()
    personality = models.TextField()
    scenario = models.TextField()
    examples_of_dialogue = models.TextField()
    custom_role_template_type = models.CharField(max_length=50)

    def __str__(self):
        return self.role_name