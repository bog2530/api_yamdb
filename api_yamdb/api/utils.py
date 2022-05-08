import uuid

from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


def message_sign_up(username, code, email):
    send_mail(
        'Sign Up.',
        f'Hi {username}. Code: {code}',
        settings.FROM_EMAIL,
        [email],
        fail_silently=False,
    )


def create_code():
    return str(uuid.uuid4())[0:16]


def create_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        "token": str(refresh.access_token)
    }


def common_permission(request, methods):
    return (
        request.method in permissions.SAFE_METHODS
        or (
            request.method in methods
            and request.user.is_authenticated
            and (
                request.user.role == User.ADMIN
                or request.user.is_superuser
            )
        )
    )
