# Generated by Django 4.2.4 on 2023-08-18 03:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='has_confirmed',
        ),
    ]
