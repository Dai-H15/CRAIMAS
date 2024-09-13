from django.urls import path
from . import views
urlpatterns = [
    path("calendar_main/", views.calendar_main, name="calendar_main"),
    path("get_calendar/<str:year>/<str:month>/<str:status>", views.get_calendar, name="get_calendar"),
    path("new_task/", views.new_task, name="new_task"),
]
