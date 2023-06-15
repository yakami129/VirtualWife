from django.utils import timezone
from ..dto.competition_dto import CompetitionDTO
from ..models import Competition


def create_competition(competition_dto: CompetitionDTO):
    ## 构建比赛实体
    competition = Competition(
        name = competition_dto.name,
        turn = competition_dto.turn,
        victor_name = competition_dto.victor_name,
        start_date = timezone.now(),
    )
    competition.save();
    return {'id':competition.id,'name':competition.name}