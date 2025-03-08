from django.contrib import admin
from .models import CustomUser, Doctor

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    ordering = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'is_staff']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    pass

