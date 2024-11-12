from django.contrib import admin
from .models import SupportTicketModel
from django.contrib import messages

# Register your models here.


class SupportTicketModelAdmin(admin.ModelAdmin):
    model = SupportTicketModel
    list_display = ("posted_at", "title", "category", "request_by__U_ID",  "is_solved", "TicketID")
    list_display_links = ("title",)
    search_fields = ["request_by__U_ID", "TicketID"]
    actions = ["accept_user"]

    def accept_user(self, request, queryset):
        queryset.update(is_solved=True)
        self.message_user(request, f"{len(queryset)}件に対して操作を実行しました", messages.SUCCESS)
    accept_user.short_description = "選択したサポートチケットをクローズ"


admin.site.register(SupportTicketModel, SupportTicketModelAdmin)
