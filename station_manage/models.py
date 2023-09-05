import datetime
from django.db import models
from group_manage.models import *
from user_info.models import *


class Works(models.Model):
    workId = models.AutoField(primary_key=True)
    workName = models.CharField(max_length=32)
    isDelete = models.BooleanField(default=False)
    groupIs = models.ForeignKey(Group, on_delete=models.CASCADE)
    leader=models.CharField(max_length=32,default="")
    create_time=models.DateTimeField(default=datetime.datetime.now())
    workCondition=models.CharField(max_length=32,default="")
    workIntroduction=models.TextField(default="")

    class Meta:
        db_table = "works"


class Pages(models.Model):
    pageId = models.AutoField(primary_key=True)
    pageName = models.CharField(max_length=32)
    workIs = models.ForeignKey(Works, on_delete=models.CASCADE)

    class Meta:
        db_table = "pages"

class Files(models.Model):
    fileId = models.AutoField(primary_key=True)
    fileName = models.CharField(max_length=32)
    fileInclude = models.TextField(default="")
    fileUrl = models.CharField(max_length=255)
    fileIs = models.ForeignKey(Works, on_delete=models.CASCADE,default="5")
    folderIs=models.IntegerField(default="0")
    class Meta:
        db_table = "files"


class Folders(models.Model):
    folderId=models.AutoField(primary_key=True)
    folderName=models.CharField(max_length=255)
    file_is_work=models.IntegerField(default="9")
    class Meta:
        db_table = "folders"
# 拥有编辑文档权限的用户


"""
自动建表,表名为app01_userinfo,同时自动添加一行主键：
id bigint auto_increment primary key 
修改表时,若要新增一列,新增列必须指定值:1.手动输入值2.设置默认值default=..3.允许为空null=True blank=True
"""
