from django.shortcuts import render, HttpResponse
from main.views import collect_regnum, collect_regsets
import calendar
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from main.models import Interview, RegistSets

# Create your views here.


def get_listInterview(request, year, month, status, search):
    interview = Interview.objects.filter(by_U_ID=request.user.U_ID).filter(date__year=year).filter(date__month=month)
    if search != "search":
        registid = RegistSets.objects.get(by_U_ID=request.user.U_ID, RegistID=search)
        interview = interview.filter(RegistID=registid)
    if (status == "active"):
        jsons = [{"Interview": i, "date": timezone.make_naive(i.date).day} for i in interview.filter(RegistID__isActive=True)]
    else:
        jsons = [{"Interview": i, "date": timezone.make_naive(i.date).day} for i in interview]

    return jsons


@login_required
def calendar_main(request):
    contexts = collect_regnum(request)
    year = timezone.make_naive(timezone.now()).year
    month = timezone.make_naive(timezone.now()).month
    today = timezone.make_naive(timezone.now()).day
    contexts["company_list"] = collect_regsets(request.user).order_by("-isActive")
    contexts["def_year"] = year
    contexts["def_month"] = month
    contexts["today"] = today
    return render(request, "task_calendar/main.html", contexts)


@login_required
def get_calendar(request, year, month, status, search):
    contexts = {}
    calendar.setfirstweekday(calendar.SUNDAY)
    list_calendar = calendar.monthcalendar(int(year), int(month))
    contexts["list_calendar"] = list_calendar
    try:
        contexts["list_interview"] = get_listInterview(request, year, month, status, search)
    except (RegistSets.DoesNotExist, Interview.DoesNotExist):
        return HttpResponse("不正な操作を検出しました。")
    if year == str(timezone.make_naive(timezone.now()).year) and month == str(timezone.make_naive(timezone.now()).month):
        contexts["today"] = timezone.make_naive(timezone.now()).day
        contexts["feature"] = False
    elif year >= str(timezone.make_naive(timezone.now()).year) and month > str(timezone.make_naive(timezone.now()).month):
        contexts["feature"] = True
    return render(request, "task_calendar/calendar_base.html", contexts)


@login_required
def new_task(request):
    contexts = collect_regnum(request)
    sets = collect_regsets(request.user)
    contexts["sets"] = sets
    return render(request, "task_calendar/new_task.html", contexts)
