from django.contrib import admin
from django.urls import path, include

from accounts.views import *

app_name = 'accounts'
urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('auth/', auth, name='auth'),
    path('verify_email/', verify_email, name='verify_email'),
    path('dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('verify_code/', verify_code, name='verify_code'),
    path('create_new_password/', create_new_password, name='create_new_password'),
    path('profile/', profile, name='profile')
]