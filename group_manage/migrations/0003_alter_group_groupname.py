# Generated by Django 3.2 on 2023-08-25 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_manage', '0002_group_groupname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='groupName',
            field=models.CharField(max_length=128),
        ),
    ]