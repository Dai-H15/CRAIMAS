from django.db import models


class CustomSheet(models.Model):
    sheet_id = models.CharField(max_length=100, primary_key=True, unique=True)
    by_U_ID = models.CharField(max_length=100, default="default")
    sheet_name = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    selected_field = models.JSONField()
    view_settings = models.JSONField()
    search_settings = models.JSONField()

    def __str__(self):
        return self.sheet_name

    class Meta:
        verbose_name = 'カスタムシート'
        verbose_name_plural = 'カスタムシート'

