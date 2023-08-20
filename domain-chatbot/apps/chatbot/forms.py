from django import forms
from .models import CustomRoleModel

class CustomRoleForm(forms.ModelForm):
    class Meta:
        model = CustomRoleModel
        fields = ['role_name', 'persona', 'personality', 'scenario', 'examples_of_dialogue', 'custom_role_template_type']
