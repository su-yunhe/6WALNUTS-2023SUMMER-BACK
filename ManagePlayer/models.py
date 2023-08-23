from django.db import models


# Create your models here.
class Player(models.Model):
    playerId = models.AutoField(primary_key=True)
    playerName = models.CharField(max_length=128, unique=True)
    playerAge = models.CharField(max_length=128)
    playerHeight = models.IntegerField()
    playerWeight = models.IntegerField()
    playerPosition = models.CharField(max_length=128)

    def __str__(self):
        return self.playerName

    class Meta:
        db_table = 'players'
        # verbose_name = '用户'
        # verbose_name_plural = verbose_name
