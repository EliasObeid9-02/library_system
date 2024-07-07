# Generated by Django 4.2.11 on 2024-07-06 17:54

from django.conf import settings
import django.contrib.auth.password_validation
from django.db import migrations, models
import django.db.models.deletion
import user_auth.validators


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0002_alter_user_options_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'A user with that email already exists'}, max_length=254, unique=True, validators=[user_auth.validators.validate_email]),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, validators=[django.contrib.auth.password_validation.validate_password]),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=150, primary_key=True, serialize=False, validators=[user_auth.validators.validate_username]),
        ),
        migrations.CreateModel(
            name='ResetToken',
            fields=[
                ('reset_token', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reset_token', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
