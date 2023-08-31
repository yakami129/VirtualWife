from django.shortcuts import render
import os
import json
import logging
from django.http import FileResponse
from .translation import translationClient
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tts.tts_core import create_audio
from django.http import HttpResponse, StreamingHttpResponse
logging.basicConfig(level=logging.INFO)


@api_view(['POST'])
def generate(request):
    """
    Generate audio from text.
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
        text = data["text"]
        voice = data["voice"]

        file_name = create_audio(text, voice)
        pwd_path = os.getcwd()
        file_path = os.path.join(pwd_path, "tmp", file_name)

        # Open the audio file in binary mode.
        audio_file = open(file_path, 'rb')

        # Create a FileResponse with a custom __del__ method to delete the file after streaming.
        class DeletableFileResponse(FileResponse):
            def __del__(self):
                delete_file(file_path)
                print("delete file :", file_path)

        # Create the response object.
        response = DeletableFileResponse(audio_file, content_type='audio/mpeg')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'

        return response
    except Exception as e:
        print(f"generate_audio error: {e}")
        return HttpResponse(status=500, content="Failed to generate audio.")


def delete_file(file_path):
    os.remove(file_path)


@api_view(['POST'])
def translation(request):
    """
    translation
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
        text = data["text"]
        target_language = data["target_language"]
        target_result = translationClient.translation(
            text=text, target_language=target_language)
        return Response({"response": target_result, "code": "200"})
    except Exception as e:
        print(f"translation error: {e}")
        return HttpResponse(status=500, content="Failed to translation error.")
