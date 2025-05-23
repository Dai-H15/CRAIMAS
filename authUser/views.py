from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
import secrets
import datetime
# Create your views here.


def signup_view(request):
    contexts = {}
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if len(user.username) < 5:
                contexts["message"] = "ユーザー名を5文字以上で設定してください"
                contexts["form"] = form
                return render(request, "registration/signup.html", contexts)
            user.U_ID = secrets.token_hex(32)
            user.is_active = False
            user.save()
            contexts["U_ID"] = user.U_ID
            contexts["username"] = user.username
            return render(request, "registration/signup_done.html", contexts)

    else:
        form = SignupForm()

    contexts = {"form": form}

    return render(request, "registration/signup.html", contexts)


def done_view(request):
    pass


def login_view(request):
    contexts = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, "registration/login_redirect.html", contexts)
            else:
                contexts["status"] = {"results": "error", "message": "ユーザーが見つかりませんでした。メールアドレスとパスワードを確認してください。"}
        else:
            contexts["status"] = {"results": "NG", "message": "資格情報が無効です。入力値を確認してください。"}
    else:
        form = LoginForm()

    contexts["form"] = form
    return render(request, "registration/new_login.html", contexts)


def policy_view(request):
    contexts = {}
    return render(request, "registration/policy.html", contexts)


@login_required
def extension_view(request):
    contexts = {}
    user = request.user
    contexts["ExpiryDate"] = user.ExpiryDate
    contexts["l_days"] = (user.ExpiryDate - datetime.date.today()).days
    contexts["ExtensionDate"] = (user.ExpiryDate + datetime.timedelta(days=30)) if contexts["l_days"] < 20 else "有効日数が20日以上です。"
    contexts["can_extension"] = True if contexts["l_days"] < 20 else False
    if request.method == "POST":
        if contexts["can_extension"]:
            user.ExpiryDate = user.ExpiryDate + datetime.timedelta(days=30)
            user.save()
            return HttpResponse('<script>window.opener.location.reload();</script>')
    return render(request, "registration/extension.html", contexts)
