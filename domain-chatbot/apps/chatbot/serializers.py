from rest_framework import serializers
from .models import CustomRoleModel, BackgroundImageModel, VrmModel, RolePackageModel


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


class UploadedRolePackageModelSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(required=False)
    dataset_json_path = serializers.CharField(required=False)
    embed_index_idx_path = serializers.CharField(required=False)
    system_prompt_txt_path = serializers.CharField(required=False)

    class Meta:
        model = RolePackageModel
        fields = '__all__'
