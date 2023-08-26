from abc import ABC, abstractmethod
from .character import Character


class BaseCharacterTemplate(ABC):

    '''统一自定义角色模版抽象类,基于当前抽象类扩展其他的自定义角色模版'''

    @abstractmethod
    def format(self, character: Character) -> str:
        pass
