from abc import ABC, abstractmethod


class BaseTranslationClient(ABC):

    '''统一翻译抽象类,基于当前抽象类扩展其他的翻译模块'''

    @abstractmethod
    def translation(self, text: str, target_language: str) -> str:
        '''翻译'''
        pass
