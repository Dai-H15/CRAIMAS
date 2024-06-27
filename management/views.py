from django.shortcuts import render, HttpResponse, redirect
from main.views import collect_regnum
from main.models import RegistSets, Interview
from authUser.models import CustomUser
from django.contrib.auth.decorators import login_required, permission_required
from .forms import InfomationForm, ManagementSupportForm
from .models import InfomationModel
from support.models import SupportTicketModel
# Create your views here.


@login_required
@permission_required("authUser.is_staff")
def management(request):
    contexts = collect_regnum(request)
    return render(request, "index.html", contexts)


@login_required
@permission_required("authUser.is_staff")
def all_sheets(request):
    if request.user.is_staff:
        contexts = collect_regnum(request)
        count = RegistSets.objects.all().count()
        contexts["count"] = count
    else:
        return HttpResponse("error: 権限がありません")

    return render(request, "all_sheets.html", contexts)


@login_required
@permission_required("authUser.is_staff")
def management_sheets(request):
    contexts = collect_regnum(request)
    return render(request, "management_sheets.html", contexts)


@login_required
@permission_required("authUser.is_staff")
def all_interviewer(request):
    contexts = collect_regnum(request)
    return render(request, "all_interviewer.html", contexts)


@login_required
@permission_required("authUser.is_staff")
def admin_all_sheet(request, sheet_from, where):
    contexts = collect_regnum(request)
    if request.user.is_staff:
        res = RegistSets.objects.all().order_by("-isActive")
        contexts["posts"] = res
        if sheet_from == "企業名":
            res = res.filter(company__name__contains=where)
        if sheet_from == "所属業界名":
            res = res.filter(company__industry__contains=where)
        if sheet_from == "所在地":
            res = res.filter(d_company__location__contains=where)
        if sheet_from == "担当者名":
            res = res.filter(company__contact__contains=where)
        if sheet_from == "ユーザー名":
            try:
                res = res.filter(by_U_ID=CustomUser.objects.get(username=where).U_ID)
            except (CustomUser.DoesNotExist, AttributeError):
                return HttpResponse("<div class = 'alert alert-warning m-3 text-center'><b>対象のユーザーが見つかりませんでした。IDを確かめてください</b></div>")
        contexts["posts"] = res
        post_interviews = {}
        for post in res:
            i = Interview.objects.filter(RegistID=post).order_by("-date").first()
            post_interviews[post.RegistID] = i.InterviewID if i is not None else None
        contexts["post_interviews"] = post_interviews
    else:
        return HttpResponse("error: 権限がありません。")
    return render(request, "admin_sheetview.html", contexts)


@login_required
@permission_required("authUser.is_staff")
def create_infomation(request):
    contexts = collect_regnum(request)
    if request.user.is_superuser:
        if request.method == "POST":
            form = InfomationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(to="create_infomation")
            else:
                contexts["form"] = form
                return render(request, "infomation.html", contexts)
        form = InfomationForm()
        contexts["infomations"] = InfomationModel.objects.all().order_by("-is_active")
        contexts["form"] = form
        return render(request, "infomation.html", contexts)
    else:
        return redirect(to="index")


@login_required
@permission_required("authUser.is_staff")
def conf_infomation(request):
    if request.user.is_superuser:
        if request.POST.get("operation") == "delete":
            s = delete_infomation(request)
        elif request.POST.get("operation") == "change_show":
            s = change_show_infomation(request)
        elif request.POST.get("operation") == "change_public":
            s = change_public(request)
        return s
    else:
        return redirect(to="index")


@login_required
@permission_required("authUser.is_staff")
def delete_infomation(request):
    InfomationModel.objects.get(id=request.POST.get("id")).delete()
    return redirect("create_infomation")


@login_required
@permission_required("authUser.is_staff")
def change_show_infomation(request):
    info = InfomationModel.objects.get(id=request.POST.get("id"))
    info.is_active = True if not info.is_active else False
    info.save()
    return redirect("create_infomation")


@login_required
@permission_required("authUser.is_staff")
def change_public(request):
    info = InfomationModel.objects.get(id=request.POST.get("id"))
    info.is_public = True if not info.is_public else False
    info.save()
    return redirect("create_infomation")


@login_required
@permission_required("authUser.is_staff")
def management_support(request):
    contexts = {}
    choice = ManagementSupportForm()
    contexts["choice"] = choice
    return render(request, "support.html", contexts)


@login_required
@permission_required("authUser.is_staff")
def support_catgory(request, select):
    contexts = {}
    if (select == "-------") or (select == "init"):
        ticket = SupportTicketModel.objects.all().order_by("is_solved")
    else:
        ticket = SupportTicketModel.objects.filter(category=select).order_by("is_solved")
    contexts["ticket"] = ticket
    return render(request, "support_category.html", contexts)


@login_required
@permission_required("authUser.is_staff")
def management_support_detail(request):
    contexts = {}
    if request.method == "POST":
        try:
            ticket = SupportTicketModel.objects.get(TicketID=request.POST.get("TicketID"))
            contexts["ticket"] = ticket
            contexts["request_by"] = CustomUser.objects.get(U_ID=ticket.request_by.U_ID)
            return render(request, "support_detail.html", contexts)
        except (SupportTicketModel.DoesNotExist, AttributeError):
            return HttpResponse("サポートチケットが見つかりませんでした")
    else:
        return HttpResponse("不正なリクエストです")


@login_required
@permission_required("authUser.is_staff")
def management_support_change_is_solved(request):
    if request.method == "POST":
        try:
            ticket = SupportTicketModel.objects.get(TicketID=request.POST.get("TicketID"))
            ticket.is_solved = not ticket.is_solved
            ticket.save()
        except (SupportTicketModel.DoesNotExist, AttributeError):
            return HttpResponse("サポートチケットが見つかりませんでした")
    return redirect("management_support")


@login_required
@permission_required("authUser.is_staff")
def support_edit_admin_comment(request):
    if request.method == "POST":
        try:
            ticket = SupportTicketModel.objects.get(TicketID=request.POST.get("TicketID"))
            ticket.admin_memo = request.POST.get("admin_memo")
            ticket.save()
        except (SupportTicketModel.DoesNotExist, AttributeError):
            return HttpResponse("サポートチケットが見つかりませんでした")
    return redirect("management_support")