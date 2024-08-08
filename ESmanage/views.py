from django.shortcuts import render, HttpResponse
from main.views import collect_regnum
from django.contrib.auth.decorators import login_required
from .forms import ESModelForm
import secrets
from .models import ESModel
# Create your views here.


@login_required
def index(request):
    contexts = collect_regnum(request)
    return render(request, "ESmanage/index.html", contexts)


@login_required
def regist(request):
    contexts = collect_regnum(request)
    form = ESModelForm()
    contexts["form"] = form
    if request.method == "POST":
        post = ESModelForm(request.POST)
        if post.is_valid():
            data = post.save(commit=False)
            data.ESModelID = secrets.token_hex(64)
            data.by_U_ID = request.user.U_ID
            data.save()
            contexts["status"] = "success"
            contexts["message"] = "登録が正常に完了しました"
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
def get_data(request):
    contexts = {}
    posts = ESModel.objects.all().filter(by_U_ID=request.user.U_ID)
    contexts["posts"] = posts
    return render(request, "ESmanage/show_table.html", contexts)


@login_required
def show_detail(request, id):
    contexts = collect_regnum(request)
    try:
        init = ESModel.objects.get(by_U_ID=request.user.U_ID, ESModelID=id)
    except ESModel.DoesNotExist:
        return HttpResponse("不正な操作です。管理者へお問い合わせください")
    form = ESModelForm(initial={"title": init.title, "tag": init.tag, "desc": init.desc})
    if request.method == "POST":
        form = ESModelForm(request.POST)
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
    return render(request, "ESmanage/show_detail.html", contexts)


@login_required
def search(request, to, what):
    contexts = {}
    try:
        if to == "タイトル":
            posts = ESModel.objects.all().filter(by_U_ID=request.user.U_ID).filter(title__contains=what)
        elif to == "タグ":
            posts = ESModel.objects.all().filter(by_U_ID=request.user.U_ID).filter(tag__contains=what)
        contexts["posts"] = posts
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
    form = ESModelForm(initial={"title": init.title, "tag": init.tag, "desc": init.desc})
    contexts["form"] = form
    if request.method == "POST":
        ESModel.objects.get(by_U_ID=request.user.U_ID, ESModelID=id).delete()
        contexts["status"] = "success"
    return render(request, "ESmanage/delete.html", contexts)
