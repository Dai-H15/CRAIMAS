from django.db import models

# Create your models here.


class InfomationModel(models.Model):
    C_CATEGORY = (
        ("news", "お知らせ"),
        ("maintenance", "メンテナンス"),
        ("release", "リリース"),
        ("other", "その他"),
        )
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=C_CATEGORY, )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
