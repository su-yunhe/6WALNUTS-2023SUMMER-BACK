from django.db import models

class Prototypes(models.Model):
    protoId=models.AutoField(primary_key=True)
    protoInclude=models.TextField(default="")
    protoName=models.CharField(max_length=32)
    workIs=models.IntegerField(default="0")
    is_vaild=models.BooleanField(default="1")
    class Meta:
        db_table = "prototypes"

