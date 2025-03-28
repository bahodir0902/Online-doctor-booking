"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from medicine.views import *
from accounts.views import doctor_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('make-appointment/', make_appointment, name='make_appointment'),
    path('get-doctors/', get_doctors, name='get_doctors'),
    path('get-available-datetime/', get_available_datetime, name='get_available_datetime'),
    path('get-available-dates/', get_available_dates, name='get_available_dates'),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', doctor_dashboard, name='doctor_dashboard')

]
