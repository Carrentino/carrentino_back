import random

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


def authenticate_user(email, password):
    '''Authorize user'''
    user = get_object_or_404(User, email=email)
    authenticated_user = authenticate(
        username=user.username, password=password)
    if authenticated_user is None:
        raise AuthenticationFailed('Invalid password')
    return authenticated_user


def update_password(email, new_password):
    '''Updating password'''
    user = get_object_or_404(User, email=email)
    user.password = make_password(new_password)
    user.save()


def generate_code():
    code = ''.join([str(random.randint(0, 9)) if i > 0 else str(
        random.randint(1, 9)) for i in range(6)])
    return code
