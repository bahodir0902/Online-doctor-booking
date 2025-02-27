from datetime import timedelta
from typing import override, Any
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings

def is_valid_rate(value) -> None:
    if not (1 <= value <= 5):
        raise ValidationError('Rate must be between 1 and 5.')


class Department(models.Model):
    name = models.CharField(max_length=50)

    @override
    def __str__(self) -> str:
        return f'{self.name}'

class Doctor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    experienced_years = models.IntegerField(default=0)
    biography = models.TextField()

    @override
    def __str__(self) -> str:
        return f'{self.user.first_name} - {self.user.last_name} - {self.department_id}'

class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        CONFIRMED = 'Confirmed', 'Confirmed'
        CANCELED = 'Canceled', 'Canceled'
        COMPLETED = 'Completed', 'Completed'

    datetime = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    class Meta:
        unique_together = ('doctor', 'datetime')

    @override
    def __str__(self) -> str:
        return f"Appointment with {self.doctor.user.first_name} at {self.datetime} ({self.status})"

class Notification(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    @override
    def __str__(self) -> str:
        return f'{self.title} - {self.content}'

class Feedback(models.Model):
    content = models.TextField()
    rate = models.SmallIntegerField(validators=[is_valid_rate])
    appointment_id = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    @override
    def __str__(self) -> str:
        return f"{self.rate} - {self.content}"


class Availability(models.Model):
    class Days_of_week(models.TextChoices):
        MONDAY = 'Monday', 'Monday'
        TUESDAY = 'Tuesday', 'Tuesday'
        WEDNESDAY = 'Wednesday', 'Wednesday'
        THURSDAY = 'Thursday', 'Thursday'
        FRIDAY = 'Friday', 'Friday'
        SATURDAY = 'Saturday', 'Saturday'
        SUNDAY = 'Sunday', 'Sunday'
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    days_of_week = models.CharField(max_length=15, choices=Days_of_week.choices)

    class Meta:
        unique_together = ('doctor', 'days_of_week')

    @override
    def __str__(self) -> str:
        return f"{self.days_of_week} ({self.start_time} to {self.end_time})"


# class User(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=20, null=True, blank=True)
#     username = models.CharField(max_length=100, null=True, blank=True)
#     password = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_doctor = models.BooleanField(default=False)
#
#     @override
#     def __str__(self) -> str:
#         return f'{self.first_name} - {self.last_name} - {self.username}'