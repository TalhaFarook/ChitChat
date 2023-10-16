# Generated by Django 4.2.5 on 2023-10-11 10:23

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("chat", "0004_onechat_is_delivered"),
    ]

    operations = [
        migrations.AlterField(
            model_name="onechat",
            name="sender_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_chat",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="GroupChat",
            fields=[
                ("message_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "message_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("message", models.TextField()),
                (
                    "receivers",
                    models.ManyToManyField(
                        related_name="received_messages", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "sender_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="group_chat",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
