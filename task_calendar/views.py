from django.shortcuts import render
from main.views import collect_regnum
import calendar
import datetime
# Create your views here.


def calendar_main(request):
    contexts = collect_regnum(request)
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    list_calendar = calendar.monthcalendar(year, month)
    contexts["list_calendar"] = list_calendar
    return render(request, "task_calendar/main.html", contexts)


