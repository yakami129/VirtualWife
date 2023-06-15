from django.utils import timezone
from ..dto.competition_record_dto import CompetitionRecordDTO
from ..models import CompetitionRecord


class CompetitionRecordHandle:

    @classmethod
    def create(competition_record_dto: CompetitionRecordDTO):
        competition_record = CompetitionRecord(
            competition_id = competition_record_dto.competition_id,
            participant_name = competition_record_dto.participant_name,
            score = competition_record_dto.score
        )
        competition_record.save()
        return competition_record
    
    @classmethod
    def update(competition_record_dto: CompetitionRecordDTO):
        competition_record = CompetitionRecord(
            id = competition_record_dto.id,
            competition_id = competition_record_dto.competition_id,
            participant_name = competition_record_dto.participant_name,
            score = competition_record_dto.score
        )
        competition_record.save()
        return competition_record


class CompetitionRecordQuery:

    @classmethod
    def getByParticipantNameAndCompetitionId(competition_id:int,participant_name:str):
        return CompetitionRecord.objects.get(competition_id=competition_id,participant_name=participant_name)
    
    @classmethod
    def getMaxScoreCompetitionRecord(competition_id:int):
        return  CompetitionRecord.objects.filter(competition_id=competition_id).order_by('-score').first()

