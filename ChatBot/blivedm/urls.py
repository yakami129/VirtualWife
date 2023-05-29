from django.urls import path
from . import views

urlpatterns = [
    path('start', views.start, name='start'),
    path('stop', views.stop, name='stop'),
]