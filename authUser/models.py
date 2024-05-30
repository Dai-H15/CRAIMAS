from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Create your models here.


class CustomUser(AbstractUser):
    U_ID = models.CharField(max_length=100)
    y_graduation = models.IntegerField()
    gBIZINFO_key = models.CharField(max_length=100)
    ExpiryDate = models.DateField(null=False, blank=False, default=datetime.date.today() + datetime.timedelta(days=20), verbose_name="アカウント利用期限")
    REQUIRED_FIELDS = ["email", "y_graduation", "gBIZINFO_key"]

    def is_account_expired(self):
        return self.ExpiryDate < datetime.date.today()

    def save(self, *args, **kwargs):
        if self.is_account_expired():
            self.is_active = False
        super().save(*args, **kwargs)