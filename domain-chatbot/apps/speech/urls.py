from django.urls import path
from . import views

urlpatterns = [
    path('tts/generate', views.generate, name='generate'),
    path('translation', views.translation, name='translation'),
]
