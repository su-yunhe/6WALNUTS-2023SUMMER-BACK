from django.utils import timezone

from django.db import models

from user_info.models import UserInfo


class Group(models.Model):
    groupId = models.AutoField(primary_key=True)
    groupName = models.CharField(max_length=128)
    groupBuilder = models.CharField(max_length=128, default='new_group')
    buildTime = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'groups'


# 中间表
class GroupUsers(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    groupId = models.ForeignKey(Group, on_delete=models.CASCADE)
    userType = models.IntegerField()

    class Meta:
        db_table = 'groupUsers'







