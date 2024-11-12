from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.index, name="ES_index"),
    path("regist/", views.regist, name="ES_regist"),
    path("show/", views.show, name="ES_show"),
    path("get_data/<str:page_num>", views.get_data, name="ES_get_data"),
    path("show_detail/<str:id>", views.show_detail, name="ES_show_detail"),
    path("search/<str:to>/<str:what>/<str:page_num>", views.search, name="ES_search"),
    path("delete/<str:id>", views.delete, name="ES_delete"),
    path("save/<str:id>", views.save_by_js, name="save_by_js")
]
