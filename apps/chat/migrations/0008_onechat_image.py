# Generated by Django 4.2.5 on 2023-10-11 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_remove_groupchat_group_groupchat_receivers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='onechat',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='chat/images/'),
        ),
    ]