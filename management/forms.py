from django import forms
from .models import InfomationModel


class InfomationForm(forms.ModelForm):
    class Meta:
        model = InfomationModel
        fields = ("title", "category", "content", "is_active")
        labels = {
            "title": "タイトル",
            "category": "カテゴリ",
            "content": "内容",
            "is_active": "公開"
        }