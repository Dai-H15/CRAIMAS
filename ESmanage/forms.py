from django import forms
from .models import ESModel


class ESModelForm(forms.ModelForm):
    class Meta:
        model = ESModel
        fields = ["title", "desc", "tag"]
        labels = {
            "title": "登録名",
            "desc": "詳細",
            "tag": "タグ"
        }
