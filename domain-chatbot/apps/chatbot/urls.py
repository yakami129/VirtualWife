from django.urls import path

from . import views

urlpatterns = [
    path('chat', views.chat, name='chat'),
    path('memory/reflection', views.reflection_generation, name='reflection_generation'),
    path('memory/clear', views.clear_memory, name='clear_memory')
]
