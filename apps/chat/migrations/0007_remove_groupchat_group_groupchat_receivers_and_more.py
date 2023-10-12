# Generated by Django 4.2.5 on 2023-10-11 13:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0006_group_remove_groupchat_receivers_groupchat_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupchat',
            name='group',
        ),
        migrations.AddField(
            model_name='groupchat',
            name='receivers',
            field=models.ManyToManyField(related_name='received_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Group',
        ),
    ]
