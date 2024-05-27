from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    U_ID = models.CharField(max_length=100)
    y_graduation = models.IntegerField()
    gBIZINFO_key = models.CharField(max_length=100)
    REQUIRED_FIELDS = ["email", "y_graduation", "gBIZINFO_key"]
