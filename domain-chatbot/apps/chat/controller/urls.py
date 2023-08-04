from django.urls import path

from . import views

urlpatterns = [
    path('chat', views.chat, name='chat'),
    path('translation',views.translation,name='translation')
]

