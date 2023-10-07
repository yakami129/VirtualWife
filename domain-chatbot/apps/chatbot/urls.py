from django.urls import path

from . import views

urlpatterns = [
    path('chat', views.chat, name='chat'),
    path('memory/reflection', views.reflection_generation,
         name='reflection_generation'),
    path('memory/clear', views.clear_memory, name='clear_memory'),
    path('customrole/list', views.custom_role_list, name='custom_role_list'),
    path('customrole/create', views.create_custom_role, name='custom_role_create'),
    path('customrole/edit/<int:pk>', views.edit_custom_role, name='custom_role_edit'),
    path('customrole/detail/<int:pk>', views.custom_role_detail, name='custom_role_detail'),
    path('customrole/delete/<int:pk>', views.delete_custom_role, name='custom_role_delete'),
    path('config/get', views.get_config, name='get_config'),
    path('config/save', views.save_config, name='save_config'),
    path('config/background/delete/<int:pk>', views.delete_background_image, name='delete_background_image'),
    path('config/background/upload', views.upload_background_image, name='upload_background_image'),
    path('config/background/show', views.show_background_image, name='show_background_image'),
    path('config/vrm/delete/<int:pk>', views.delete_vrm_model, name='delete_vrm_model'),
    path('config/vrm/upload', views.upload_vrm_model, name='upload_vrm_model'),
    path('config/vrm/user/show', views.show_user_vrm_models, name='show_user_vrm_models'),
    path('config/vrm/system/show', views.show_system_vrm_models, name='show_system_vrm_models'),
]
