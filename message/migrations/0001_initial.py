# Generated by Django 3.2 on 2023-08-25 08:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('group_manage', '0005_delete_message'),
        ('user_info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('messageId', models.AutoField(primary_key=True, serialize=False)),
                ('senderId', models.IntegerField()),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.TextField()),
                ('groupId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group_manage.group')),
            ],
            options={
                'db_table': 'message',
            },
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=False)),
                ('messageId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='message.message')),
                ('targetId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_info.userinfo')),
            ],
            options={
                'db_table': 'user_message',
            },
        ),
    ]
