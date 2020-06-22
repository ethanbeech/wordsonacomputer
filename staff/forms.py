from django import forms
from .models import StaffMember
from django.contrib.auth.models import User

class StaffUpdateForm(forms.ModelForm):
    class Meta:
        model = StaffMember
        fields = ['full_name', 'description', 'profile_picture']
