from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils import timezone

# Create your models here.


class CustomUser(AbstractUser):
    U_ID = models.CharField(max_length=100)
    y_graduation = models.IntegerField()
    gBIZINFO_key = models.CharField(max_length=100)
    ExpiryDate = models.DateField(null=False, blank=False, default=datetime.date.today() + datetime.timedelta(days=20), verbose_name="アカウント利用期限")
    infomation_last_checked = models.DateTimeField(null=False, blank=False, default=datetime.strptime("2020-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"), verbose_name="お知らせ最終確認日時")
    REQUIRED_FIELDS = ["last_name", "first_name", "email", "y_graduation", "gBIZINFO_key"]
