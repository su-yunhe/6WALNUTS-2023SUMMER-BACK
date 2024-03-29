# Generated by Django 3.2 on 2023-08-25 12:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('station_manage', '0002_delete_file_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='fileIs',
            field=models.ForeignKey(default='5', on_delete=django.db.models.deletion.CASCADE, to='station_manage.works'),
        ),
        migrations.AddField(
            model_name='works',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 25, 20, 46, 55, 805592)),
        ),
        migrations.AddField(
            model_name='works',
            name='leader',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AddField(
            model_name='works',
            name='workCondition',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AddField(
            model_name='works',
            name='workIntroduction',
            field=models.TextField(default=''),
        ),
    ]
