from django import forms
from .models import InfomationModel


CATEGORY = (
    ("-------", "-------"),
    ("mypage", "マイページに関して"),
    ("del_account", "アカウントの削除・退会"),
    ("bug", "バグ・不具合の問い合わせ、報告"),
    ("want", "機能追加の要望等"),
    ("mod_account", "アカウント情報の編集等"),
    ("sheet", "企業情報等の登録に関して"),
    ("help", "操作方法等の問い合わせ"),
    ("other", "その他の問い合わせ"),
)


class InfomationForm(forms.ModelForm):
    class Meta:
        model = InfomationModel
        fields = ("title", "category", "content", "is_active", "is_public")
        labels = {
            "title": "タイトル",
            "category": "カテゴリ",
            "content": "内容",
            "is_active": "公開",
            "is_public": "全体に公開"
        }


class ManagementSupportForm(forms.Form):
    choices = forms.ChoiceField(choices=CATEGORY, label="絞り込み")
