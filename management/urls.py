from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.management, name="management"),
    path("all_sheets/", views.all_sheets, name="all_sheets"),
    path("management_sheets/", views.management_sheets, name="management_sheets"),
    path("all_interviewer", views.all_interviewer, name="all_interviewer"),
    path("admin_all_sheet/<str:sheet_from>/<str:where>", views.admin_all_sheet, name="admin_all_sheet"),
]
