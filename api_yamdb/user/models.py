from django.contrib.auth.models import AbstractUser
from django.db import models

from api.utils import UsernameValeidationMixin

ADMIN = 'admin'
USER = 'user'
MODERATOR = 'moderator'


class User(UsernameValeidationMixin, AbstractUser):
    ROLE_LIST = [
        (ADMIN, 'admin'),
        (USER, 'user'),
        (MODERATOR, 'moderator'),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_LIST, default=USER)
    bio = models.TextField(blank=True)
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELDS = 'email'

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return str(self.username)
