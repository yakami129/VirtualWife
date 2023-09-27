from rest_framework import serializers
from .models import CustomRoleModel, BackgroundImageModel,VrmModel

class CustomRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomRoleModel
        fields = '__all__'

class UploadedImageSerializer(serializers.ModelSerializer):

    original_name = serializers.CharField(required=False)

    class Meta:
        model = BackgroundImageModel
        fields = '__all__'

class UploadedVrmModelSerializer(serializers.ModelSerializer):

    original_name = serializers.CharField(required=False)
    type = serializers.CharField(required=False)

    class Meta:
        model = VrmModel
        fields = '__all__'
