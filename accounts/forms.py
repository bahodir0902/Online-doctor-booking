from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from typing import override
from django.conf import settings

class UserRegisterModelForm(forms.ModelForm):
    re_password = forms.CharField(max_length=200, widget=forms.PasswordInput)
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password', 're_password']
        widgets={
            'password': forms.PasswordInput
        }

    @override
    def clean(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password != re_password:
            raise ValidationError(params=password, message='Passwords don\'t match.')
        return self.cleaned_data

class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=200, widget=forms.EmailInput)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput)

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = get_user_model().objects.filter(email=email).first()
        if not user:
            raise ValidationError('User doesn\'t exists.')

        return email


class PassCodeVerification(forms.Form):
    code = forms.CharField(max_length=10)


class UserProfileModelForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'username']
        widgets = {
            'email': forms.EmailInput
        }

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if get_user_model().objects.filter(email=email).exists():
    #         raise ValidationError('User with this email already exists')
    #     return email