from django.contrib.auth.models import AbstractUser
from django.db import models

from api.mixins import UsernameValeidationMixin


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
    confirmation_code = models.CharField(max_length=255, null=True,
                                         blank=False, default='aaaa')
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELDS = 'email'

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    # @property
    # def is_user(self):
    #     return self.role == "user"

    def __str__(self):
        return str(self.username)
