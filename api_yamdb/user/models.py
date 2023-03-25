from django.contrib.auth.models import AbstractUser
from django.db import models

from user.validators import MyReqularValidator, validate_username

ADMIN = 'admin'
USER = 'user'
MODERATOR = 'moderator'


class User(AbstractUser):
    ROLE_EXIST = [
        (ADMIN, 'admin'),
        (USER, 'user'),
        (MODERATOR, 'moderator'),
    ]
    username = models.CharField(max_length=150, blank=False, unique=True,
                                validators=[validate_username,
                                            MyReqularValidator, ])
    email = models.EmailField(max_length=254, blank=False, unique=True,
                              null=False)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=10, choices=ROLE_EXIST, default=USER)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    confirmation_code = models.CharField(max_length=255, null=True,
                                         blank=False, default='aaaa')
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELDS = 'email'

    @property
    def is_admin(self):
        return self.role == "admin" or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == "moderator"

    @property
    def is_user(self):
        return self.role == "user"

    def __str__(self):
        return str(self.username)
