from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Define a custom user model by extending AbstractUser.
class UserTable(AbstractUser):
    id = models.AutoField(primary_key=True) # Use the 'id' field as the primary key.
    email = models.EmailField(unique=True) # Email for the user, required and must be unique.
    username = models.CharField(max_length=12, unique=True) # Username for the user, required and must be unique.
    last_login = models.DateTimeField(default = timezone.now) # Timestamp of the user's last login.
    current_active = models.BooleanField(default=False) # A boolean field to track the user's current activity status.

    # Define the 'USERNAME_FIELD' which will be used for user authentication.
    USERNAME_FIELD = 'username'

    def __str__(self):
        # This method returns the username when the user object is printed.
        return self.username
