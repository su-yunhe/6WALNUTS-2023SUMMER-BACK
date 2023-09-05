from django.db import models
from django.utils import timezone

from group_manage.models import Group
from user_info.models import UserInfo


# Create your models here.
class Chat(models.Model):
    chatId = models.AutoField(primary_key=True)
    groupId = models.ForeignKey(Group, on_delete=models.CASCADE)
    chatName = models.CharField(max_length=128, default='hhh')
    leaderId = models.IntegerField(default=0)
    chatType = models.IntegerField()

    class Meta:
        db_table = 'chat'


class Message(models.Model):
    messageId = models.AutoField(primary_key=True)
    senderName = models.CharField(max_length=128, default='user')
    chatId = models.ForeignKey(Chat, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    class Meta:
        db_table = 'message'


class UserMessage(models.Model):
    id = models.AutoField(primary_key=True)
    messageId = models.ForeignKey(Message, on_delete=models.CASCADE)
    targetId = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    state = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_message'


class TeamMessage(models.Model):
    id = models.AutoField(primary_key=True)
    adminId = models.IntegerField()
    inviteId = models.IntegerField()
    groupId = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        db_table = 'team_message'


class ChatMessage(models.Model):
    id = models.AutoField(primary_key=True)
    adminId = models.IntegerField()
    inviteId = models.IntegerField()
    chatId = models.IntegerField(default=0)
    chatName = models.CharField(max_length=128, default='chat')
    type = models.IntegerField(default=0)

    class Meta:
        db_table = 'chat_message'


class ChatUser(models.Model):
    id = models.AutoField(primary_key=True)
    chatId = models.ForeignKey(Chat, on_delete=models.CASCADE)
    userId = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'chat_user'


