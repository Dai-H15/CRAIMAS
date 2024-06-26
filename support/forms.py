from django import forms
from .models import SupportTicketModel


class SupportForm(forms.ModelForm):
    class Meta:
        model = SupportTicketModel
        fields = ("category", "title", "text")
        labels = {
            "category": "お問い合わせカテゴリー",
            "title": "問い合わせタイトル",
            "text": "問い合わせ内容",
        }
