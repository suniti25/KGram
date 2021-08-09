from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class UserModel(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    follows = models.ManyToManyField('user.UserModel', blank=True)
    image = models.CharField(max_length=255, blank=True)
    otp = models.CharField(max_length = 6, blank =True)