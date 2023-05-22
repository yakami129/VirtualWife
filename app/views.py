from django.shortcuts import render
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .core.cat_lady_chat_robot import CatLady


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
        chat = CatLady.chat(query=data["query"])
    except Exception as e:
        print("chat error: %s" % str(e))
        chat = '发生系统错误，请稍后重试'
    return Response({"response": chat, "code": "200"})