from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    Roles = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    ]

    bio = models.TextField(
        'Biography',
        blank=True,
    )

    role = models.CharField(
        max_length=32,
        choices=Roles,
        default=USER,
        verbose_name='Роль'
    )

    email = models.EmailField(
        'E-mail',
        max_length=254,
        unique=True,
        null=False,
    )

    confirmation_code = models.TextField(
        'confirmation code',
        max_length=16,
        null=True,
    )

    @property
    def admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
