from django.utils import timezone
from ..dto.competition_record_dto import CompetitionRecordDTO
from ..models import CompetitionRecord


class CompetitionRecordHandle:

    @classmethod
    def create(cls,competition_record_dto: CompetitionRecordDTO):
        competition_record = CompetitionRecord(
            competition_id = competition_record_dto.competition_id,
            participant_name = competition_record_dto.participant_name,
            score = competition_record_dto.score
        )
        competition_record.save()
        return competition_record
    
    @classmethod
    def update(cls,competition_record_dto: CompetitionRecordDTO):
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
    def getByCompetitionIdAndParticipantName(cls,competition_id:int,participant_name:str):
        try:
            return CompetitionRecord.objects.get(competition_id=competition_id, participant_name=participant_name)
        except CompetitionRecord.DoesNotExist:
            return None
       
    
    @classmethod
    def getMaxScoreCompetitionRecord(cls,competition_id:int):
        return CompetitionRecord.objects.filter(competition_id=competition_id).order_by('-score').first()

