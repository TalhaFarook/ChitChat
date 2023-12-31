# Generated by Django 4.2.5 on 2023-10-12 08:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0017_alter_onechat_receiver_id_alter_onechat_sender_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='receivers',
            field=models.ManyToManyField(related_name='received_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
