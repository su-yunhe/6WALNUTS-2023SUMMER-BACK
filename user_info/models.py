from django.db import models


# Create your models here.
class UserInfo(models.Model):
    userId = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=128,unique=True)
    userPassword = models.CharField(max_length=128)
    userEmail = models.EmailField(unique=True)
    userRealName = models.CharField(max_length=128)

    def __str__(self):
        return self.userName

    class Meta:
        db_table = 'users'
        # verbose_name = '用户'
        # verbose_name_plural = verbose_name
