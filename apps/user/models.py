from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class UserTable(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    username = models.CharField(max_length=12, unique=True)
    last_login = models.DateTimeField(default=timezone.now)
    current_active = models.BooleanField(default=False)

    # Define the 'USERNAME_FIELD' which will be used for user authentication.
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username
