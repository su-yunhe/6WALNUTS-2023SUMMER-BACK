# Generated by Django 3.2 on 2023-08-30 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_manage', '0011_rename_folderid_file_vers_folderis'),
    ]

    operations = [
        migrations.CreateModel(
            name='File_model',
            fields=[
                ('fileId', models.IntegerField()),
                ('fileName', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('fileInclude', models.TextField(default='')),
            ],
            options={
                'db_table': 'file_model',
            },
        ),
    ]