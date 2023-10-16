from django.db import models
from django.utils import timezone

from apps.user.models import UserTable


class OneChat(models.Model):
    message_id = models.AutoField(primary_key=True)
    message_time = models.DateTimeField(default=timezone.now)
    receiver_id = models.ForeignKey(
        UserTable, on_delete=models.CASCADE, related_name="user_chat"
    )
    sender_id = models.PositiveIntegerField()
    image = models.ImageField(upload_to="", blank=True, null=True, max_length=255)
    message = models.TextField()
    is_sent = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.sender_id


class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    receivers = models.ManyToManyField(UserTable, related_name="received_messages")
    group_name = models.CharField(max_length=255)

    def __str__(self):
        return self.group_name


class GroupChat(models.Model):
    message_id = models.AutoField(primary_key=True)
    message_time = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to="", blank=True, null=True, max_length=255)
    sender_id = models.ForeignKey(
        UserTable, on_delete=models.CASCADE, related_name="group_chats"
    )
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="group_messages"
    )
    message = models.TextField()

    def __str__(self):
        return self.sender_id
