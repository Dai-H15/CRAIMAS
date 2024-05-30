from django.db.models.signals import pre_save, post_init
from django.dispatch import receiver
from .models import CustomUser
from django.contrib.auth.hashers import make_password
import datetime


@receiver(pre_save, sender=CustomUser)
def change_password(sender, instance, **kwargs):
    try:  # ユーザーが存在する場合の処理
        user = CustomUser.objects.get(username=instance.username)
        if instance.password != user.password:
            print('changed')
            instance.password = make_password(instance.password)
    except CustomUser.DoesNotExist:
        pass


@receiver(post_init, sender=CustomUser)
def is_account_expired(sender, instance, **kwargs):
    if instance.ExpiryDate < datetime.date.today():
        instance.is_active = False
