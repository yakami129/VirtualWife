from django.urls import path
from . import views

urlpatterns = [
    path('tts/generate', views.generate, name='generate'),
    path('tts/voices', views.get_voices, name='voices'),
    path('translation', views.translation, name='translation'),
]
