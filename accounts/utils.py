import random
import uuid
import pandas as pd
import os

from django.shortcuts import redirect

from config import settings


def generate_random_code():
    code = str(random.randint(1000, 9999))
    return code

def generate_unique_username():
    # Generate a random unique identifier and trim it if needed
    return uuid.uuid4().hex[:30]

def login_required(REDIRECT_FIELD_NAME='accounts:login'):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return func(request, *args, **kwargs)
            return redirect(REDIRECT_FIELD_NAME)

        return wrapper
    return decorator


def has_permission(ROLE):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.role == ROLE:
                    return func(request, *args, **kwargs)

        return wrapper
    return decorator


def export_excel(users_list):
    path = os.path.join(settings.MEDIA_ROOT, 'exported/users_lists')
    df = pd.DataFrame(users_list)
    df.to_excel('users_list.xlsx', index=False)
    return path

