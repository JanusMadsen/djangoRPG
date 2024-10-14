from django.db import models
from django.contrib.auth.models import User
from random import randint


# Create your models here.
class player_model(models.Model):
    Strength = models.IntegerField(default=0)
    Weight= models.IntegerField(default=0)
    AC = models.IntegerField(default=10)
    HP = models.IntegerField(default=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)

class goblin(models.Model):
    Strengthlvl = models.IntegerField(default=8)
    HP = models.IntegerField(default=7)
    AC = models.IntegerField(default=15)
