from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import CustomUser
from django.contrib.auth.hashers import make_password

"""
@receiver(pre_save, sender=CustomUser)
def change_password(sender, instance, **kwargs):
    user = CustomUser.objects.get(username=instance.username)
    if instance.password != user:
        instance.password = make_password(instance.password)"""