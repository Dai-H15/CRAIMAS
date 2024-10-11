from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path("done/", views.done_view, name="signup_done"),
    path("policy/", views.policy_view, name="policy"),
    path("extension/", views.extension_view, name="extension"),
]
