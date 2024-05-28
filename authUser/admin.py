from django.contrib import admin
from .models import CustomUser

# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ("is_active", "username", "U_ID", "y_graduation", "is_staff", "is_superuser", "date_joined")
    list_display_links = ("username", "U_ID")
    search_fields = ["username", "email", "U_ID"]


admin.site.register(CustomUser, CustomUserAdmin)
