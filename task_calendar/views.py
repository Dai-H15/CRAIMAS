from django.shortcuts import render
from main.views import collect_regnum
import calendar
import datetime
from main.models import Interview
# Create your views here.


def get_listInterview(request, year, month):
    return [{"Interview": i, "date": i.date.day} for i in Interview.objects.filter(by_U_ID=request.user.U_ID).filter(date__year=year).filter(date__month=month)]


def calendar_main(request):
    contexts = collect_regnum(request)
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    calendar.setfirstweekday(calendar.SUNDAY)
    list_calendar = calendar.monthcalendar(year, month)
    contexts["list_calendar"] = list_calendar
    today = datetime.datetime.now().day
    contexts["def_year"] = year
    contexts["def_month"] = month
    contexts["today"] = today
    contexts["list_interview"] = get_listInterview(request, year, month)
    return render(request, "task_calendar/main.html", contexts)


def get_calendar(request, year, month):
    contexts = collect_regnum(request)
    calendar.setfirstweekday(calendar.SUNDAY)
    list_calendar = calendar.monthcalendar(int(year), int(month))
    contexts["list_calendar"] = list_calendar
    contexts["list_interview"] = get_listInterview(request, year, month)
    if year == str(datetime.datetime.now().year) and month == str(datetime.datetime.now().month):
        contexts["today"] = datetime.datetime.now().day
    return render(request, "task_calendar/calendar_base.html", contexts)


