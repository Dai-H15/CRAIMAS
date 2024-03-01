from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("regist_base/", views.regist_base, name="regist_base"),
    path("regist_base/regist_all/", views.regist_all, name="regist_all"),
    path("show/", views.show_data, name="show"),
    path("mypage/", views.mypage, name="mypage"),
]