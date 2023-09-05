
from user_info.models import *
from group_manage.models import *
from station_manage.models import *

class File_Users(models.Model):
    fileId=models.ForeignKey(Files, on_delete=models.CASCADE)
    userId=models.ForeignKey(UserInfo,on_delete=models.CASCADE)

    class Meta:
        db_table = "file_users"


class File_Vers(models.Model):
    fileId = models.IntegerField()
    fileName = models.CharField(max_length=32, primary_key=True)
    fileInclude = models.TextField(default="")
    fileUrl = models.CharField(max_length=255)
    fileIs = models.ForeignKey(Works, on_delete=models.CASCADE,default="5")
    fileVersion=models.IntegerField(default=1)
    folderIs=models.IntegerField(default=0)
    class Meta:
        db_table = "file_vers"

class File_Message(models.Model):
    id=models.AutoField(primary_key=True)
    sendId = models.ForeignKey(UserInfo, on_delete=models.CASCADE,related_name='sendId')
    receiveId= models.ForeignKey(UserInfo, on_delete=models.CASCADE,related_name='receiveId')
    messageIs=models.ForeignKey(Files, on_delete=models.CASCADE)

    class Meta:
        db_table = "file_message"

class File_model(models.Model):
    fileId = models.IntegerField()
    fileName = models.CharField(max_length=32, primary_key=True)
    fileInclude = models.TextField(default="")
    class Meta:
        db_table = "file_model"
