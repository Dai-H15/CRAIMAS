from django.db.models.signals import pre_save, post_init
from django.dispatch import receiver
from .models import CustomUser
from django.contrib.auth.hashers import make_password
import datetime


@receiver(post_init, sender=CustomUser)
def is_account_expired(sender, instance, **kwargs):
    if instance.ExpiryDate < datetime.date.today():
        instance.is_active = False
