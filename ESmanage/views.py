from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.urls import reverse
from main.views import collect_regnum
from django.contrib.auth.decorators import login_required
from .forms import ESModelRegistForm, ESModelConfirmForm
import secrets
from .models import ESModel
from django.utils import timezone
from django.core.paginator import Paginator

# Create your views here.


@login_required
def index(request):
    contexts = collect_regnum(request)
    return render(request, "ESmanage/index.html", contexts)


@login_required
def regist(request):
    contexts = collect_regnum(request)
    form = ESModelRegistForm()
    contexts["form"] = form
    if request.method == "POST":
        post = ESModelRegistForm(request.POST)
        if post.is_valid():
            data = post.save(commit=False)
            data.ESModelID = secrets.token_hex(64)
            data.by_U_ID = request.user.U_ID
            data.save()
            contexts["ESModelID"] = data.ESModelID
            return render(request, "ESmanage/open_confirm_window.html", contexts)
        else:
            contexts["status"] = "danger"
            contexts["message"] = "登録が完了しませんでした。入力内容を確かめてください"
            contexts["form"] = post
    return render(request, "ESmanage/regist.html", contexts)


@login_required
def show(request):
    contexts = collect_regnum(request)
    return render(request, "ESmanage/show.html", contexts)


@login_required
def get_data(request, page_num):
    contexts = {}
    posts = ESModel.objects.all().filter(by_U_ID=request.user.U_ID).order_by("-created")
    paginator = Paginator(posts, 5)
    page_count = paginator.num_pages
    try:
        page_num = int(page_num)
    except ValueError:
        return HttpResponse("不正な操作を検出しました。")
    if (0 < page_num <= page_count):
        page = paginator.page(page_num)
    else:
        page = paginator.page(1)
    contexts["request_url"] = reverse("ES_get_data", kwargs={
                        "page_num": "page_num"
                })
    contexts["posts"] = page
    contexts["page_count"] = page_count
    contexts["page_num"] = page_num
    return render(request, "ESmanage/show_table.html", contexts)


@login_required
def show_detail(request, id):
    contexts = collect_regnum(request)
    try:
        init = ESModel.objects.get(by_U_ID=request.user.U_ID, ESModelID=id)
    except ESModel.DoesNotExist:
        return HttpResponse("不正な操作です。管理者へお問い合わせください")
    form = ESModelConfirmForm(initial={"title": init.title, "tag": init.tag, "desc": init.desc})
    if request.method == "POST":
        form = ESModelConfirmForm(request.POST)
        if form.is_valid():
            init.title = form.cleaned_data['title']
            init.tag = form.cleaned_data['tag']
            init.desc = form.cleaned_data['desc']
            init.save()
            contexts["status"] = "success"
            contexts["message"] = "編集が完了しました"
        else:
            contexts["status"] = "danger"
            contexts["message"] = "エラーが発生しました。内容を確認してください"
    contexts["form"] = form
    contexts["ESModelID"] = init.ESModelID
    return render(request, "ESmanage/show_detail.html", contexts)


@login_required
def search(request, to, what, page_num):
    contexts = {}
    try:
        if to == "タイトル":
            posts = ESModel.objects.all().filter(by_U_ID=request.user.U_ID).filter(title__contains=what)
        elif to == "タグ":
            posts = ESModel.objects.all().filter(by_U_ID=request.user.U_ID).filter(tag__contains=what)
        paginator = Paginator(posts, 5)
        page_count = paginator.num_pages
        try:
            page_num = int(page_num)
        except ValueError:
            return HttpResponse("不正な操作を検出しました。")
        if (0 < page_num <= page_count):
            page = paginator.page(page_num)
        else:
            page = paginator.page(1)
        contexts["request_url"] = reverse("ES_search", kwargs={
                        "to": to,
                        "what": what,
                        "page_num": "page_num"
                })
        contexts["posts"] = page
        contexts["page_count"] = page_count
        contexts["page_num"] = page_num
    except UnboundLocalError:
        return HttpResponse("エラーが発生しました。管理者までお問い合わせください<br><a href = '/'> ホームへ戻る </a>")
    return render(request, "ESmanage/show_table.html", contexts)


@login_required
def delete(request, id):
    contexts = collect_regnum(request)
    try:
        init = ESModel.objects.get(by_U_ID=request.user.U_ID, ESModelID=id)
    except ESModel.DoesNotExist:
        return HttpResponse("エラーが発生しました。管理者までお問い合わせください<br><a href = '/'> ホームへ戻る </a>")
    form = ESModelConfirmForm(initial={"title": init.title, "tag": init.tag, "desc": init.desc})
    contexts["form"] = form
    if request.method == "POST":
        ESModel.objects.get(by_U_ID=request.user.U_ID, ESModelID=id).delete()
        contexts["status"] = "success"
    return render(request, "ESmanage/delete.html", contexts)


@login_required
def save_by_js(request, id):
    contexts = {
        "status": "",
        "message": "",
        "saved_time": "",
    }
    try:
        init = ESModel.objects.get(by_U_ID=request.user.U_ID, ESModelID=id)
    except ESModel.DoesNotExist:
        contexts["saved_time"] = "None"
        contexts["message"] = "不正な操作です"
        contexts["is_saved"] = "NG"
        return JsonResponse(contexts)
    if request.method == "POST":
        form = ESModelConfirmForm(request.POST)
        if form.is_valid():
            init.title = form.cleaned_data['title']
            init.tag = form.cleaned_data['tag']
            init.desc = form.cleaned_data['desc']
            init.save()
            contexts["is_saved"] = "OK"
            contexts["message"] = "編集が完了しました"
            contexts["saved_time"] = timezone.datetime.now().time()
        else:
            contexts["is_saved"] = "danger"
            contexts["message"] = "エラーが発生しました。内容を確認してください"
            contexts["saved_time"] = timezone.datetime.now().time()
    return JsonResponse(contexts)


@login_required
def view_ES_interview(request, id):
    contexts = collect_regnum(request)
    esmodel = ESModel.objects.get(by_U_ID=request.user.U_ID, ESModelID=id)
    contexts["ESModel"] = esmodel
    return render(request, "ESmanage/view_interview.html", contexts)


@login_required
def get_ES_interview(request, id, setting):
    contexts = {}
    esmodel = ESModel.objects.get(by_U_ID=request.user.U_ID, ESModelID=id)
    interviews = esmodel.interview_set.filter(by_U_ID=request.user.U_ID)
    if setting == "act":
        interviews = interviews.filter(RegistID__isActive=True)
    contexts["interviews"] = interviews
    return render(request, "ESmanage/interview_result.html", contexts)
