from drf_yasg import openapi

competition_record_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'competition_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='比赛id'),
        'participant_name': openapi.Schema(type=openapi.TYPE_STRING, description='比赛参与者'),
        'score': openapi.Schema(type=openapi.TYPE_INTEGER, description='比赛分数')
    },
    required=['competition_id', 'participant_name', 'score'],
)


class CompetitionRecordDTO:
    
    def __init__(self,id, competition_id, participant_name, score):
        self.id = id
        self.competition_id = competition_id
        self.participant_name = participant_name
        self.score = score

    @classmethod
    def from_dict(cls, data):
        return cls(
            competition_id=data.get('competition_id'),
            participant_name=data.get('participant_name'),
            score=data.get('score')
        )