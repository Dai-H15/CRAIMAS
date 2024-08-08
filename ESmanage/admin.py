from django.contrib import admin
from .models import ESModel
# Register your models here.


class ESModelAdmin(admin.ModelAdmin):
    model = ESModel
    list_display = ("title", "desc", "ESModelID", "by_U_ID")
    search_fields = ["title", "by_U_ID", "ESModelID"]


admin.site.register(ESModel, ESModelAdmin)
