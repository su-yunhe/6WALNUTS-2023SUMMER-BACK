# Generated by Django 3.2 on 2023-08-25 12:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('station_manage', '0003_auto_20230825_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='works',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 25, 20, 47, 17, 356978)),
        ),
    ]
