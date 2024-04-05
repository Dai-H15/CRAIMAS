from django.urls import path
from . import views

urlpatterns = [
    path("view_index/", views.view_index, name="view_index"),
    path("view_main/<str:control>/<str:option>", views.view_main, name="view_main"),
    path("create_custom_sheet", views.create_custom_sheet, name="create_custom_sheet"),
    path("delete_custom_sheet/<str:id>", views.delete_custom_sheet, name="delete_custom_sheet"),
    path("export_customsheet/", views.export_customsheet, name="export_customsheet"),
    path("import_customsheet/", views.import_customsheet, name="import_customsheet"),
]
