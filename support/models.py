from django.db import models
from authUser.models import CustomUser
# Create your models here.

CATEGORY = (
    ("mypage", "マイページに関して"),
    ("del_account", "アカウントの削除・退会"),
    ("bug", "バグ・不具合の問い合わせ、報告"),
    ("want", "機能追加の要望等"),
    ("mod_account", "アカウント情報の編集等"),
    ("sheet", "企業情報等の登録に関して"),
    ("help", "操作方法等の問い合わせ"),
    ("other", "その他の問い合わせ"),
)


class SupportTicketModel(models.Model):
    TicketID = models.CharField(max_length=200, primary_key=True, unique=True, verbose_name="チケットID")
    category = models.CharField(choices=CATEGORY, max_length=32, blank=False, null=False, verbose_name="カテゴリー")
    title = models.CharField(max_length=64, verbose_name="タイトル")
    text = models.TextField(verbose_name="問い合わせ内容")
    request_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, verbose_name="問い合わせ元")
    posted_at = models.DateTimeField(auto_now_add=True)
    admin_memo = models.TextField(verbose_name="管理者メモ")
    is_solved = models.BooleanField(default=False, verbose_name="クローズフラグ")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'サポートチケット'
        verbose_name_plural = 'サポートチケット'
