from django.shortcuts import render
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .service.competition_service import *
from .service.competition_record_service import *
from .dto.competition_dto import *
from .dto.competition_record_dto import *
from django.utils.dateparse import parse_datetime
from drf_yasg.utils import swagger_auto_schema
from .service.game_service import start_competition;

# Create your views here.
@swagger_auto_schema(method='post', request_body=competition_request_body)
@api_view(['POST'])
def create_competition_req(request):
    '''
      创建比赛
    :param request:
    :return:
    '''
    data = json.loads(request.body.decode('utf-8'))
    data['start_date'] = parse_datetime(data['start_date'])
    data['end_date'] = parse_datetime(data['end_date'])
    competition_dto = CompetitionDTO.from_dict(data)
    db_competition = CompetitionHandle.create(competition_dto)
    return Response({"response": db_competition, "code": "200"})


@swagger_auto_schema(method='GET')
@api_view(['GET'])
def start_game(request):
    '''
      开始你画我猜游戏
    '''
    start_competition()
    return Response({"response": '开始游戏', "code": "200"})


