from django.urls import path

from . import views

urlpatterns = [
    path('chat', views.chat, name='chat'),
    path('memory/reflection', views.reflection_generation,
         name='reflection_generation'),
    path('memory/clear', views.clear_memory, name='clear_memory'),
    path('customrole/list', views.custom_role_list, name='custom_role_list'),
    path('customrole/create', views.custom_role_create, name='custom_role_create'),
    path('customrole/edit/<int:pk>', views.custom_role_edit, name='custom_role_edit'),
    path('customrole/detail/<int:pk>', views.custom_role_detail, name='custom_role_detail'),
    path('customrole/delete/<int:pk>', views.custom_role_delete, name='custom_role_delete'),
    path('customrole/vrmmodel/list', views.vrm_model_list, name='vrm_model_list'),
    path('config/get', views.get_config, name='get_config'),
    path('config/save', views.save_config, name='save_config'),
]
