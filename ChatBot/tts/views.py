from django.shortcuts import render
import os
import json
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tts.tts_core import createAudio
from django.http import HttpResponse, FileResponse
logging.basicConfig(level=logging.INFO)

@api_view(['POST'])
def generateAudio(request):
    '''
      合成语音
    :param request:
    :return:
    '''
    data = json.loads(request.body.decode('utf-8'))
    text = data["text"]
    voice = data["voice"]
    file_name = createAudio(text, voice)
    pwdPath = os.getcwd()
    file_path = pwdPath + "/tmp/" + file_name

    # 设置HTTP响应头部
    # 打开音频文件进行流式传输
    audio_file = open(file_path, 'rb')

    # 使用FileResponse进行流式传输
    response = FileResponse(audio_file, content_type='audio/mpeg')
    response['Content-Disposition'] = 'attachment; filename="audio.mp3"'

    return response
