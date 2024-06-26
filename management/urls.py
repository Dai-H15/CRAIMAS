from django.urls import path
from . import views

urlpatterns = [
    path("", views.management, name="management"),
    path("all_sheets/", views.all_sheets, name="all_sheets"),
    path("management_sheets/", views.management_sheets, name="management_sheets"),
    path("all_interviewer", views.all_interviewer, name="all_interviewer"),
    path("admin_all_sheet/<str:sheet_from>/<str:where>", views.admin_all_sheet, name="admin_all_sheet"),
    path("infomation/", views.create_infomation, name="create_infomation"),
    path("conf_infomation/", views.conf_infomation, name="conf_infomation"),
    path("management_support/", views.management_support, name="management_support"),
    path("support_catgory/<str:select>", views.support_catgory, name="support_catgory"),
    path("management_support_detail/", views.management_support_detail, name="management_support_detail"),
    path("management_support_change_is_solved", views.management_support_change_is_solved, name="management_support_change_is_solved"),
    path("support_edit_admin_comment/", views.support_edit_admin_comment, name="support_edit_admin_comment")
]
