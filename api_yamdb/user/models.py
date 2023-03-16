from django.contrib.auth.models import AbstractUser
from django.db import models
from user.validators import validate_username
# username,email,role,bio,first_name,last_name


ADMIN='ADMIN'
USER='USER'
MODERATOR='MODERATOR'

class User(AbstractUser):

    ROLE_EXIST = [
        (ADMIN,'admin'),
        (USER,'user'),
        (MODERATOR,'moderator'),
    ]
    username = models.CharField(
        max_length=50,
        blank=False,
        unique=True,
        validators=[validate_username],
    )
    email = models.EmailField(
        blank=False,
        unique=True,
        null=False
    )
    bio = models.TextField(
        blank=True,
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_EXIST,
        default=USER
    )
    first_name = models.CharField(
        max_length=30,
        blank=True
    )
    last_name = models.CharField(
        max_length=30,
        blank=True
    )
