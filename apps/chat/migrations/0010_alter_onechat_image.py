# Generated by Django 4.2.5 on 2023-10-11 13:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0009_alter_onechat_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="onechat",
            name="image",
            field=models.ImageField(upload_to="chat\\images"),
        ),
    ]
