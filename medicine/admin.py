from django.contrib import admin
from medicine.models import *

# Register your models here.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    pass

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    pass

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass