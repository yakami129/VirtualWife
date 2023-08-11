from django.shortcuts import render
import os
import json
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tts_core import create_audio
from django.http import HttpResponse, FileResponse, StreamingHttpResponse
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
        response.closed = audio_file.close
        return response
    except Exception as e:
        print(f"generate_audio error: {e}")
        return HttpResponse(status=500, content="Failed to generate audio.")
   
  
