# Generated by Django 3.2 on 2023-08-26 02:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('station_manage', '0005_alter_works_create_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='works',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 26, 10, 48, 33, 296807)),
        ),
    ]
