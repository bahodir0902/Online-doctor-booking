from django.db import models
from typing import override
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    class UserRole(models.TextChoices):
        ADMIN = 'admin', ' Admin'
        USER = 'user', 'User'
        DOCTOR = 'doctor', 'Doctor'

    phone_number = models.CharField(max_length=255)
    email = models.EmailField(unique=True, blank=False)
    role = models.CharField(max_length=50, choices=UserRole.choices, default=UserRole.USER)


    @override
    def __str__(self):
        return self.get_full_name()

def default_expire_date():
    return timezone.now() + timedelta(minutes=1)


class CodePassword(models.Model):
    code_number = models.CharField(max_length=10)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expire_date = models.DateTimeField(default=default_expire_date)

    @override
    def save(self, *args, **kwargs):
        CodePassword.objects.filter(user=self.user).delete()
        super().save(*args, **kwargs)

    @override
    def __str__(self):
        return f"Code: {self.code_number} for {self.user.email} (Expires: {self.expire_date})"


class CodeEmail(models.Model):
    code_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=200)
    expire_date = models.DateTimeField(default=default_expire_date)

    @override
    def save(self, *args, **kwargs):
        CodeEmail.objects.filter(email=self.email).delete()
        super().save(*args, **kwargs)

    @override
    def __str__(self):
        return f"Code: {self.code_number} for {self.email} (Expires: {self.expire_date})"
