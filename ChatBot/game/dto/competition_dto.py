from drf_yasg import openapi

competition_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='比赛名称'),
        'turn': openapi.Schema(type=openapi.TYPE_INTEGER, description='比赛轮次'),
        'victor_name': openapi.Schema(type=openapi.TYPE_STRING, description='胜利者名称'),
        'start_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='比赛开始时间'),
        'end_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='比赛结束时间'),
    },
    required=['name', 'turn', 'victor_name', 'start_date', 'end_date'],
)

class CompetitionDTO:
    def __init__(self, id=None, name=None, turn=None, victor_name=None, start_date=None, end_date=None):
        self.id = id
        self.name = name
        self.turn = turn
        self.victor_name = victor_name
        self.start_date = start_date
        self.end_date = end_date

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get('name'),
            turn=data.get('turn'),
            victor_name=data.get('victor_name'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date')
        )
    

    

    

