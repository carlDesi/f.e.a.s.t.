# Generated by Django 3.2 on 2024-04-10 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_userprofile_adminroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='subrooms',
            field=models.JSONField(default=dict),
        ),
    ]