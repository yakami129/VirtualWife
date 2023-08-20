from django.shortcuts import render
import os
import json
import logging
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

        # Use FileResponse to stream the file.
        response = StreamingHttpResponse(audio_file, content_type='audio/mpeg')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'

        # Attach a callback to close the file when the response is finished.
        response.closed = lambda: (
            audio_file.close(),
            delete_file(file_path)
        )
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
