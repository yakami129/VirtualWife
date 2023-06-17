from django.urls import path
from . import views

urlpatterns = [
    path('generateAudio', views.generate_audio, name='generate_audio'),
]