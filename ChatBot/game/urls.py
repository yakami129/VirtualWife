from django.urls import path

from . import views

urlpatterns = [
    path('create_competition', views.create_competition_req, name='create_competition'),
]
