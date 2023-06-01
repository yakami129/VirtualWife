from django.urls import path
from . import views

urlpatterns = [
    path('generateAudio', views.generateAudio, name='generateAudio'),
]