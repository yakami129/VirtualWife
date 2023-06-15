from drf_yasg import openapi

leaderboard_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'participant_name': openapi.Schema(type=openapi.TYPE_STRING, description='比赛参与者'),
        'wins': openapi.Schema(type=openapi.TYPE_INTEGER, description='获胜次数')
    },
    required=['participant_name', 'wins'],
)

class LeaderboardDTO:
    def __init__(self, participant_name, wins):
        self.participant_name = participant_name
        self.wins = wins

    @classmethod
    def from_dict(cls, data):
        return cls(
            participant_name=data.get('participant_name'),
            wins=data.get('wins'),
        )