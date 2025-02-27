from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model

class UserLoginForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']
        widgets={
            'email': forms.EmailInput(attrs={'class': 'form-label'}),
            'password': forms.PasswordInput(attrs={'class': 'form-label'})
        }
        error_messages = {
            'email': {'Invalid': 'Email is invalid'}
        }