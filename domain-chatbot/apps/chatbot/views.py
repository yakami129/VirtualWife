import os
import time
from django.conf import settings
from django.shortcuts import render, get_object_or_404
import json
from .serializers import CustomRoleSerializer, UploadedImageSerializer, UploadedVrmModelSerializer
from .process import process_core
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .config import singleton_sys_config
from .reflection.reflection_generation import ReflectionGeneration
from .models import CustomRoleModel, BackgroundImageModel, VrmModel
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def chat(request):
    '''
      聊天
    :param request:
    :return:
    '''
    data = json.loads(request.body.decode('utf-8'))
    query = data["query"]
    you_name = data["you_name"]
    process_core.chat(you_name=you_name, query=query)
    return Response({"response": "OK", "code": "200"})


@api_view(['POST'])
def save_config(request):
    '''
      保存系统配置
    :param request:
    :return:
    '''
    data = json.loads(request.body.decode('utf-8'))
    config = data["config"]
    singleton_sys_config.save(config)
    singleton_sys_config.load()
    return Response({"response": config, "code": "200"})


@api_view(['GET'])
def get_config(request):
    '''
      获取系统配置
    :param request:
    :return:
    '''
    return Response({"response": singleton_sys_config.get(), "code": "200"})


@api_view(['GET'])
def reflection_generation(request):
    '''
      生成新记忆
    :return:
    '''
    rg = ReflectionGeneration()
    rg.generation(role_name="Maiko")
    timestamp = time.time()
    expr = f'timestamp <= {timestamp}'
    result = singleton_sys_config.memory_storage_driver.pageQuery(
        1, 100, expr=expr)
    return Response({"response": result, "code": "200"})


@api_view(['GET'])
def clear_memory(request):
    '''
      删除测试记忆
    :return:
    '''
    result = singleton_sys_config.memory_storage_driver.clear("alan")
    return Response({"response": result, "code": "200"})


@api_view(['GET'])
def custom_role_list(request):
    result = CustomRoleModel.objects.all()
    serializer = CustomRoleSerializer(data=result, many=True)
    serializer.is_valid()
    result = serializer.data
    return Response({"response": result, "code": "200"})


@api_view(['GET'])
def custom_role_detail(request, pk):
    role = get_object_or_404(CustomRoleModel, pk=pk)
    return Response({"response": role, "code": "200"})


@api_view(['POST'])
def create_custom_role(request):
    data = request.data  # 获取请求的 JSON 数据

    # 从 JSON 数据中提取字段值
    role_name = data.get('role_name')
    persona = data.get('persona')
    personality = data.get('personality')
    scenario = data.get('scenario')
    examples_of_dialogue = data.get('examples_of_dialogue')
    custom_role_template_type = data.get('custom_role_template_type')

    # 创建 CustomRoleModel 实例并保存到数据库
    custom_role = CustomRoleModel(
        role_name=role_name,
        persona=persona,
        personality=personality,
        scenario=scenario,
        examples_of_dialogue=examples_of_dialogue,
        custom_role_template_type=custom_role_template_type
    )
    custom_role.save()

    return Response({"response": "Data added to database", "code": "200"})


@api_view(['POST'])
def edit_custom_role(request, pk):
    data = request.data  # 获取请求的 JSON 数据
    # 从 JSON 数据中提取字段值
    id = data.get('id')
    role_name = data.get('role_name')
    role_name = data.get('role_name')
    persona = data.get('persona')
    personality = data.get('personality')
    scenario = data.get('scenario')
    examples_of_dialogue = data.get('examples_of_dialogue')
    custom_role_template_type = data.get('custom_role_template_type')

    # 更新 CustomRoleModel 实例并保存到数据库
    custom_role = CustomRoleModel(
        id=id,
        role_name=role_name,
        persona=persona,
        personality=personality,
        scenario=scenario,
        examples_of_dialogue=examples_of_dialogue,
        custom_role_template_type=custom_role_template_type
    )
    custom_role.save()
    return Response({"response": "Data edit to database", "code": "200"})


@api_view(['POST'])
def delete_custom_role(request, pk):
    role = get_object_or_404(CustomRoleModel, pk=pk)
    role.delete()
    return Response({"response": "ok", "code": "200"})


@api_view(['POST'])
def delete_background_image(request, pk):

    # 删除数据
    background_image_model = get_object_or_404(BackgroundImageModel, pk=pk)
    background_image_model.delete()

    # 获取要删除的文件路径
    file_path = os.path.join(
        settings.MEDIA_ROOT, str(background_image_model.image))
    # 删除关联的文件
    if os.path.exists(file_path):
        os.remove(file_path)

    return Response({"response": "ok", "code": "200"})


@api_view(['POST'])
def upload_background_image(request):
    """
    Upload a background image.
    """
    serializer = UploadedImageSerializer(data=request.data)
    if serializer.is_valid():
        # 获取上传文件对象
        uploaded_file = request.data['image']
        # 获取上传文件的原始文件名
        original_filename = uploaded_file.name
        serializer.save(original_name=original_filename)
        return Response({"response": "ok", "code": "200"})
    return Response({"response": "no", "code": "500"})


@api_view(['GET'])
def show_background_image(request):
    """
    Retrieve a list of uploaded background images.
    """
    images = BackgroundImageModel.objects.all()
    serializer = UploadedImageSerializer(images, many=True)
    return Response({"response": serializer.data, "code": "200"})


@api_view(['POST'])
def delete_vrm_model(request, pk):
    """
    删除VRM模型数据
    """
    # 删除数据
    vrm_model = get_object_or_404(VrmModel, pk=pk)
    vrm_model.delete()

    # 获取要删除的文件路径
    file_path = os.path.join(settings.MEDIA_ROOT, str(vrm_model.vrm))
    # 删除关联的文件
    if os.path.exists(file_path):
        os.remove(file_path)

    return Response({"response": "ok", "code": "200"})


@api_view(['POST'])
def upload_vrm_model(request):
    """
    上传VRM模型
    """
    serializer = UploadedVrmModelSerializer(data=request.data)
    if serializer.is_valid():
        # 获取上传文件对象
        uploaded_file = request.data['vrm']
        # 获取上传文件的原始文件名
        original_filename = uploaded_file.name
        serializer.save(original_name=original_filename, type="user")
        return Response({"response": "ok", "code": "200"})
    logger.error(serializer.errors)
    return Response({"response": "no", "code": "500"})


@api_view(['GET'])
def show_user_vrm_models(request):
    """
    获取VRM模型列表
    """
    vrm_models = VrmModel.objects.all()
    serializer = UploadedVrmModelSerializer(vrm_models, many=True)
    return Response({"response": serializer.data, "code": "200"})

@api_view(['GET'])
def show_system_vrm_models(request):
    '''
      获取角色模型列表
    :param request:
    :return:
    '''
    vrm_models = [
        {
            "id": "sys_01",
            "type": "system",
            "original_name": "わたあめ_03.vrm",
            "vrm": "わたあめ_03.vrm"
        },
        {
            "id": "sys_02",
            "type": "system",
            "original_name": "わたあめ_02.vrm",
            "vrm": "わたあめ_02.vrm"
        },
        {
            "id": "sys_03",
            "type": "system",
            "original_name": "hailey.vrm",
            "vrm": "hailey.vrm"
        },
        {
            "id": "sys_04",
            "type": "system",
            "original_name": "后藤仁.vrm",
            "vrm": "后藤仁.vrm"
        },
        {
            "id": "sys_05",
            "type": "system",
            "original_name": "aili.vrm",
            "vrm": "aili.vrm"
        }
    ]
    return Response({"response": vrm_models, "code": "200"})
