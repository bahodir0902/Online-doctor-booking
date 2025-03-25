from django.core.exceptions import ValidationError
from django.db import models
from typing import override
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser, Group
from django.conf import settings
from django.core.validators import FileExtensionValidator


# class UserRole(models.TextChoices):
#     ADMIN = 'admin', ' Admin'
#     USER = 'user', 'User'
#     DOCTOR = 'doctor', 'Doctor'

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=255)
    email = models.EmailField(unique=True, blank=False)

    # profile_photo = models.FilePathField()
    # role = models.CharField(max_length=50, choices=UserRole.choices, default=UserRole.USER)

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


def validate_image_size(image):
    max_size = 4 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError('Image size can\'t exceed 4 MB.')

class Doctor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey('medicine.Department', on_delete=models.SET_NULL, null=True)
    experienced_years = models.IntegerField(default=0)
    biography = models.TextField()
    # profile_photo = models.ImageField(
    #     upload_to='doctors/profile_photos',
    #     validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
    #         validate_image_size]
    # )


    class Meta:
        permissions = [
            ('can_access_doctor_dashboard', 'Can access doctor dashboard')
        ]

    @override
    def __str__(self) -> str:
        return f'{self.user.first_name} - {self.user.last_name} - {self.department_id}'
