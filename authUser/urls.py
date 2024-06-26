from django.urls import path, include
from . import views
urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("signup/", views.signup_view, name="signup"),
    path("done/", views.done_view, name="signup_done"),
    path("policy/", views.policy_view, name="policy"),
    path("extension/", views.extension_view, name="extension"),
]
