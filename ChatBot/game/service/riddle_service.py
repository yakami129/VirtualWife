from ..models import Riddle

class RiddleQuery:

    '''获取所有谜语实体'''
    @classmethod
    def all(cls):
       return Riddle.objects.all()

