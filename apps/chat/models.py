from django.db import models
from apps.user.models import UserTable
from django.utils import timezone

# Model representing a single chat message
class OneChat(models.Model):
    message_id = models.AutoField(primary_key=True)  # Unique ID for each message
    message_time = models.DateTimeField(default=timezone.now)  # Timestamp of the message
    receiver_id = models.ForeignKey(UserTable, on_delete=models.CASCADE, related_name='user_chat')  # User who sent the message and is the foreign key mapping to the UserTable's id field.
    sender_id = models.PositiveIntegerField()  # User ID of the message receiver
    image = models.ImageField(upload_to='', blank=True, null=True, max_length=255)  # Image field
    message = models.TextField()  # Text content of the message
    is_sent = models.BooleanField(default=False)  # Indicates if the message has been sent
    is_read = models.BooleanField(default=False)  # Indicates if the message has been read
    is_delivered = models.BooleanField(default=False)  # Indicates if the message has been delivered

# Model representing a group
class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    # Many-to-many relationship with UserTable to define group receivers
    receivers = models.ManyToManyField(UserTable, related_name='received_messages')
    group_name = models.CharField(max_length=255)  # Name of the group

    def __str__(self):
        # This method returns the group name when the object is printed
        return self.group_name

# Model representing group chat messages
class GroupChat(models.Model):
    message_id = models.AutoField(primary_key=True)
    message_time = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='', blank=True, null=True, max_length=255)  # Image field
    sender_id = models.ForeignKey(UserTable, on_delete=models.CASCADE, related_name='group_chats')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_messages')  # Group to which the message belongs
    message = models.TextField()  # Text content of the message