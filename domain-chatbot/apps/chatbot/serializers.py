from rest_framework import serializers
from .models import CustomRoleModel

class CustomRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomRoleModel
        fields = '__all__'