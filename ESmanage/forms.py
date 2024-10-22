from django import forms
from .models import ESModel


class ESModelRegistForm(forms.ModelForm):
    class Meta:
        model = ESModel
        fields = ["title", "tag"]
        labels = {
            "title": "登録名",
            "tag": "タグ"
        }


class ESModelConfirmForm(forms.ModelForm):
    class Meta:
        model = ESModel
        fields = ["title", "desc", "tag"]
        labels = {
            "title": "登録名",
            "desc": "詳細",
            "tag": "タグ"
        }
