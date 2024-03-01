from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.


class CustomUser(AbstractUser):
    c_id = models.CharField(max_length=100)
    y_graduation = models.IntegerField()
    

