# Generated by Django 4.2.11 on 2024-07-07 09:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0004_alter_resettoken_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resettoken',
            name='creation_time',
        ),
        migrations.AddField(
            model_name='resettoken',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 7, 9, 29, 56, 940445)),
            preserve_default=False,
        ),
    ]
