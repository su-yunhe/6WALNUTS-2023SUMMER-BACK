# Generated by Django 3.2 on 2023-09-02 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page_manage', '0003_prototypes_is_vaild'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prototypes',
            name='protoInclude',
            field=models.BinaryField(),
        ),
    ]
