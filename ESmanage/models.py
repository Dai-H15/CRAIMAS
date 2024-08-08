from django.db import models

# Create your models here.


class ESModel(models.Model):
    TAGS = (
        ("ES", "ES"),
        ("面談", "面談"),
            )
    ESModelID = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    by_U_ID = models.CharField(max_length=100, default="default")
    title = models.CharField(max_length=64, verbose_name="タイトル")
    desc = models.TextField()
    tag = models.CharField(max_length=32, choices=TAGS)

    def __str__(self) -> str:
        return self.title + "[ES Model]"

    class Meta:
        verbose_name = 'ES管理シート'
        verbose_name_plural = 'ES管理シート'
