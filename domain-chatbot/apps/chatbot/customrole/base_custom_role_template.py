from abc import ABC, abstractmethod
from .custom_role import CustomRole


class BaseCustomRoleTemplate(ABC):

    '''统一自定义角色模版抽象类,基于当前抽象类扩展其他的自定义角色模版'''

    @abstractmethod
    def format(self, custom_role: CustomRole) -> str:
        pass
