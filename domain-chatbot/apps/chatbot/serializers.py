from rest_framework import serializers
from .models import CustomRoleModel, BackgroundImageModel

class CustomRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomRoleModel
        fields = '__all__'

class UploadedImageSerializer(serializers.ModelSerializer):

    original_name = serializers.CharField(required=False)

    class Meta:
        model = BackgroundImageModel
        fields = '__all__'
