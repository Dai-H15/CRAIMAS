from django.contrib import admin
from .models import CustomUser
from django.contrib import messages
from django.utils.translation import ngettext
import datetime

# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ("is_active", "username", "U_ID", "is_staff", "is_superuser", "ExpiryDate")
    list_display_links = ("username", "U_ID")
    search_fields = ["username", "email", "U_ID"]
    actions = ["accept_user", "reject_user", "add_use_date"]

    def accept_user(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{len(queryset)}件に対して操作を実行しました", messages.SUCCESS)
    accept_user.short_description = "選択したユーザーの利用を承認"

    def reject_user(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{len(queryset)}件に対して操作を実行しました", messages.SUCCESS)
    reject_user.short_description = "選択したユーザーの利用を拒否"

    def add_use_date(self, request, queryset):
        for query in queryset:
            query.ExpiryDate = query.ExpiryDate + datetime.timedelta(days=30)
            query.is_active = True
            query.save()
        self.message_user(request, f"{len(queryset)}件に対して操作を実行しました", messages.SUCCESS)
    add_use_date.short_description = "選択したユーザーの利用期限を30日延長"


admin.site.register(CustomUser, CustomUserAdmin)
