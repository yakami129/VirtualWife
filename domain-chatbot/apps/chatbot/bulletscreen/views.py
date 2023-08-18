from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .core.zblivedm_main import start_handle,stop_handle
from asgiref.sync import async_to_sync

import asyncio
import logging
logging.basicConfig(level=logging.INFO)

@api_view(['GET'])
def start(request):
    '''
      开启直播间监听器
    :param request:
    :return:
    '''
    start_handle()
    return Response({"response": "成功", "code": "200"})

@api_view(['GET'])
def stop(request):
    '''
      关闭直播间监听器
    :param request:
    :return:
    '''
    asyncio.run(stop_handle())
    return Response({"response": "成功", "code": "200"})


