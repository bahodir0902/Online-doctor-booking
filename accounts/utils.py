import random
import uuid

from django.shortcuts import redirect


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