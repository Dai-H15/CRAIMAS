from django.urls import path
from . import views

urlpatterns = [
    path("main", views.support_post, name="support_main")
]
