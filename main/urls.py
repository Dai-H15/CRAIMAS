from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("regist_base/", views.regist_base, name="regist_base"),
    path("regist_base/regist_all/", views.regist_all, name="regist_all"),
    path("show/", views.show_data, name="show"),
    path("mypage/", views.mypage, name="mypage"),
    path("view_my_post/<str:id>", views.view_my_post, name="view_my_post"),
    path("delete_posts/<str:id>", views.delete_posts, name="delete_posts"),
    path("edit_posts/<str:id>", views.edit_posts, name="edit_posts"),
    path("regist_base/regist_sets/", views.regist_sets, name="regist_sets"),
    path("regist_base/regist_sets/create_company/", views.create_company, name="create_company"),
    path("regist_base/regist_sets/import_company/", views.import_company, name="import_company"),
    path("regist_base/regist_sets/create_about", views.create_about, name="create_about"),
    path("regist_base/regist_sets/create_idea", views.create_idea, name="create_idea"),
    path("regist_base/regist_sets/create_motivation", views.create_motivation, name="create_motivation"),
    path("regist_base/regist_sets/create_d_company", views.create_d_company, name="create_d_company"),
    path("regist_base/regist_sets/create_adoption", views.create_adoption, name="create_adoption"),
    path("regist_base/regist_sets/create_complete", views.create_complete, name="create_complete"),
]