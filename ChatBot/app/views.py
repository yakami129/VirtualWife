from django.shortcuts import render
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .core.enice_chat_robot import Enice
from .translation.translation_client import TranslationClient


# Create your views here.
@api_view(['POST'])
def chat(request):
    '''
      聊天
    :param request:
    :return:
    '''
    data = json.loads(request.body.decode('utf-8'))
    chat = None
    try:
        chat = Enice.chat(query=data["query"])
    except Exception as e:
        print("chat error: %s" % str(e))
        chat = '发生系统错误，请稍后重试'
    return Response({"response": chat, "code": "200"})

@api_view(['POST'])
def translation(request):
    '''
      翻译，中文 -> 日语
    :param request:
    :return:
    '''
    data = json.loads(request.body.decode('utf-8'))
    translation = None
    try:
        translation = TranslationClient.translation(query=data["query"])["translation"][0]
    except Exception as e:
        print("translation error: %s" % str(e))
        translation = '发生系统错误，请稍后重试'
    return Response({"response": translation, "code": "200"})