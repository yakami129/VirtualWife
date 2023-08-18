from django.urls import path
from . import views
from .bilibili import bilibili_handle

urlpatterns = [
    path('start', views.start, name='start'),
    path('stop', views.stop, name='stop'),
]