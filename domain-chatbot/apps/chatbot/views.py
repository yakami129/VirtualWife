import time
from django.shortcuts import render
import asyncio
import json
from .chat import chat_service
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .config import singleton_sys_config
from .memory.reflection.reflection_generation import ReflectionGeneration
import logging
logging.basicConfig(level=logging.INFO)


@api_view(['POST'])
def chat(request):
    '''
      聊天
    :param request:
    :return:
    '''
    data = json.loads(request.body.decode('utf-8'))
    chat = None
    query = data["query"]
    you_name = "alan"
    role_name = "爱莉"
    # try:
    #      chat = chat_service.chat(
    #          role_name=role_name, you_name=you_name, query=query)
    # except Exception as e:
    #      print("chat error: %s" % str(e))
    #      chat = '哎呀,系统小哥哥突然打了个呵欠,估计是太辛苦了需要补充能量!等他喝几口咖啡,打个盹儿,很快就会精神抖擞地回来工作的!'
    chat = chat_service.chat(
              role_name=role_name, you_name=you_name, query=query)
    return Response({"response": chat, "code": "200"})


@api_view(['GET'])
def reflection_generation(request):
    '''
      生成新记忆
    :return:
    '''
    rg = ReflectionGeneration()
    rg.generation(role_name="Maiko")
    timestamp = time.time()
    expr = f'timestamp <= {timestamp}'
    result = singleton_sys_config.memory_storage_driver.pageQuery(1, 100, expr=expr)
    return Response({"response": result, "code": "200"})


@api_view(['GET'])
def clear_memory(request):
    '''
      删除测试记忆
    :return:
    '''
    result = singleton_sys_config.memory_storage_driver.clear("alan")
    return Response({"response": result, "code": "200"})


# @api_view(['POST'])
# def translation(request):
#     '''
#       翻译，中文 -> 日语
#     :param request:
#     :return:
#     '''
#     data = json.loads(request.body.decode('utf-8'))
#     translation = None
#     try:
#         translation = TranslationClient.translation(
#             query=data["query"])["translation"][0]
#     except Exception as e:
#         print("translation error: %s" % str(e))
#         translation = '发生系统错误，请稍后重试'
#     return Response({"response": translation, "code": "200"})
