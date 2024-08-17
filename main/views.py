from django.shortcuts import render, redirect, HttpResponse

from ESmanage.forms import ESModelForm
from .models import (
    Companies,
    About,
    RegistSets,
    Idea,
    Motivation,
    D_Company,
    Adoption,
    Interview,
    Interviewer,
)
from django.db.models import Q
from ESmanage.models import ESModel
from authUser.models import CustomUser
from management.models import InfomationModel
from .forms import (
    CompaniesForm,
    AboutForm,
    ESModelSelectForm,
    IdeaForm,
    MotivationForm,
    D_CompanyForm,
    AdoptionForm,
    SearchForm_corpnum,
    InterviewForm,
    Form_Prof_Interviewer
)
import secrets
import requests
import csv
import urllib
import json
from urllib.parse import quote
from django.contrib.auth.decorators import login_required
from datetime import datetime
import datetime as dt
from django.forms.models import model_to_dict
from django.urls import reverse
from django.http import JsonResponse
from django.utils import timezone
from support.models import SupportTicketModel
# Functions


def collect_regnum(request):
    if request.user.is_authenticated:
        res = {
            "num_c": Companies.objects.filter(by_U_ID=request.user.U_ID).count(),
            "num_a": RegistSets.objects.filter(isActive=True, by_U_ID=request.user.U_ID).count(),
            "num_i": Interview.objects.filter(by_U_ID=request.user.U_ID, RegistID__isActive=True).count(),
        }
    else:
        res = {}
    return res


def collect_regsets(user):
    res = RegistSets.objects.filter(by_U_ID=user.U_ID)
    return res


def getRegistForms(RegistID, contexts, request):
    try:
        post = RegistSets.objects.get(RegistID=RegistID, by_U_ID=request.user.U_ID)
        contexts["post"] = post
        contexts["as_staff"] = False
    except RegistSets.DoesNotExist:
        if request.user.is_staff:
            post = RegistSets.objects.get(RegistID=RegistID)
            contexts["post"] = post
            contexts["as_staff"] = True
        else:
            raise AttributeError
    if post.company is not None:
        C_Form = CompaniesForm(instance=post.company)
        contexts["C_Form"] = C_Form
    if post.about is not None:
        A_Form = AboutForm(instance=post.about)
        contexts["A_Form"] = A_Form
    if post.idea is not None:
        I_Form = IdeaForm(instance=post.idea)
        contexts["I_Form"] = I_Form
    if post.motivation is not None:
        M_Form = MotivationForm(instance=post.motivation)
        contexts["M_Form"] = M_Form
    if post.d_company is not None:
        D_Form = D_CompanyForm(instance=post.d_company)
        contexts["D_Form"] = D_Form
    if post.adoption is not None:
        AD_Form = AdoptionForm(instance=post.adoption)
        contexts["AD_Form"] = AD_Form

    return contexts


# Views
def index(request):
    if "CompanyID" in request.session:
        del request.session["CompanyID"]
    if "RegistID" in request.session:
        del request.session["RegistID"]
    if "NotFound" in request.session:
        del request.session["NotFound"]
    if "forms" in request.session:
        del request.session["forms"]
    if "jsons" in request.session:
        del request.session["jsons"]
    if "Interviews" in request.session:
        del request.session["Interviews"]
    if "result_data" in request.session:
        del request.session["result_data"]
    if "Interviewers" in request.session:
        del request.session["Interviewers"]
    contexts = collect_regnum(request)
    if request.user.is_authenticated:
        contexts["infomation_news"] = InfomationModel.objects.filter(category="news", is_active=True)
        contexts["infomation_maintenance"] = InfomationModel.objects.filter(category="maintenance", is_active=True)
        contexts["infomation_release"] = InfomationModel.objects.filter(category="release", is_active=True)
        contexts["ExpirationDate"] = (request.user.ExpiryDate - dt.date.today()).days
        if request.user.is_staff:
            contexts["n_SupportTicket"] = SupportTicketModel.objects.filter(is_solved=False).count()
    else:
        contexts["infomation_news"] = InfomationModel.objects.filter(category="news", is_public=True, is_active=True)
        contexts["infomation_maintenance"] = InfomationModel.objects.filter(category="maintenance", is_public=True, is_active=True)
        contexts["infomation_release"] = InfomationModel.objects.filter(category="release", is_public=True, is_active=True)
    return render(request, "main/index.html", contexts)


@login_required
def regist_base(request):
    contexts = collect_regnum(request)
    return render(request, "main/regist/regist_base.html", contexts)


@login_required
def regist_all(request):
    contexts = collect_regnum(request)
    if request.method == "GET":
        if "forms" in request.session:
            C_Form = CompaniesForm(request.session["forms"]["C_Form"])
            A_Form = AboutForm(request.session["forms"]["A_Form"])
            D_Form = D_CompanyForm(request.session["forms"]["D_Form"])
            I_Form = IdeaForm()
            M_Form = MotivationForm()
            AD_Form = AdoptionForm()
            del request.session["forms"]
        elif "jsons" in request.session:
            C_Form = CompaniesForm(request.session["jsons"]["C_Form"])
            A_Form = AboutForm(request.session["jsons"]["A_Form"])
            I_Form = IdeaForm(request.session["jsons"]["I_Form"])
            M_Form = MotivationForm(request.session["jsons"]["M_Form"])
            D_Form = D_CompanyForm(request.session["jsons"]["D_Form"])
            AD_Form = AdoptionForm(request.session["jsons"]["AD_Form"])
            if request.session["Interviews"] != "None":
                contexts["messages"] = {
                    "color": "warning",
                    "message": "<h5>インポートされたJSON内に面談録が含まれています。</h5><h5>シートの登録完了後、面談録が登録されます。登録完了後に確認を行ってください</h5>",
                }
                if request.session["Interviewers"] != "None":
                    contexts["messages"]["message"] += "<h5>面接官情報が含まれていました。同時にインポートを行います</h5>"
            else:
                contexts["messages"] = {
                    "color": "success",
                    "message": "<h5>インポートが完了しました。内容が正しいか確認し、登録を行ってください。</h5><h5>なお、面談録は情報に含まれていませんでした。</h5>",
                }
                if request.session["Interviewers"] != "None":
                    contexts["messages"]["message"] += "<h5>面接官情報が含まれていました。同時にインポートを行います</h5>"
            del request.session["jsons"]
        else:
            C_Form = CompaniesForm()
            A_Form = AboutForm()
            D_Form = D_CompanyForm()
            I_Form = IdeaForm()
            M_Form = MotivationForm()
            AD_Form = AdoptionForm()
            if "jsons" in request.session:
                del request.session["jsons"]
            if "Interviews" in request.session:
                del request.session["Interviews"]
            if "forms" in request.session:
                del request.session["forms"]
    if request.method == "POST":
        C_Form = CompaniesForm(request.POST)
        A_Form = AboutForm(request.POST)
        I_Form = IdeaForm(request.POST)
        M_Form = MotivationForm(request.POST)
        D_Form = D_CompanyForm(request.POST)
        AD_Form = AdoptionForm(request.POST)
        if (
            C_Form.is_valid()
            and A_Form.is_valid()
            and I_Form.is_valid()
            and M_Form.is_valid()
            and D_Form.is_valid()
            and AD_Form.is_valid()
        ):
            CompanyID = secrets.token_hex(64)
            n_CForm = C_Form.save(commit=False)
            n_CForm.CompanyID = CompanyID
            n_CForm.by_U_ID = request.user.U_ID
            n_CForm.save()

            C_Data = Companies.objects.get(CompanyID=CompanyID)
            n_AForm = A_Form.save(commit=False)
            n_AForm.company_name = C_Data
            n_AForm.by_U_ID = request.user.U_ID
            n_AForm.AboutID = secrets.token_hex(64)
            n_IForm = I_Form.save(commit=False)
            n_IForm.company_name = C_Data
            n_IForm.IdeaID = secrets.token_hex(64)
            n_IForm.by_U_ID = request.user.U_ID
            n_MForm = M_Form.save(commit=False)
            n_MForm.company_name = C_Data
            n_MForm.by_U_ID = request.user.U_ID
            n_MForm.MotivationID = secrets.token_hex(64)
            n_DForm = D_Form.save(commit=False)
            n_DForm.company_name = C_Data
            n_DForm.D_CompanyID = secrets.token_hex(64)
            n_DForm.by_U_ID = request.user.U_ID
            n_ADForm = AD_Form.save(commit=False)
            n_ADForm.company_name = C_Data
            n_ADForm.AdoptionID = secrets.token_hex(64)
            n_ADForm.by_U_ID = request.user.U_ID

            n_AForm.save()
            n_IForm.save()
            n_MForm.save()
            n_DForm.save()
            n_ADForm.save()
            R_ID = secrets.token_hex(64)
            n_RegistSets = RegistSets.objects.create(
                RegistID=R_ID,
                by_U_ID=request.user.U_ID,
                company=C_Data,
                about=About.objects.get(company_name=C_Data),
                idea=Idea.objects.get(company_name=C_Data),
                motivation=Motivation.objects.get(company_name=C_Data),
                d_company=D_Company.objects.get(company_name=C_Data),
                adoption=Adoption.objects.get(company_name=C_Data),
            )
            n_RegistSets.save()
            contexts["C_Data"] = C_Data
            if "Interviews" in request.session:  # Interviewの登録
                n = 0
                if request.session["Interviews"] != "None":
                    for i in request.session["Interviews"]["interviews"]:
                        Interview.objects.create(
                            **i,
                            by_U_ID=request.user.U_ID,
                            RegistID=RegistSets.objects.get(RegistID=R_ID),
                            InterviewID=secrets.token_hex(64),
                        )
                        n += 1
                contexts["In_counts"] = n
            if "Interviewers" in request.session:
                n = 0
                if request.session["Interviewers"] != "None":
                    for i in request.session["Interviewers"]["interviewers"]:
                        Interviewer.objects.create(
                            **i,
                            company_name=RegistSets.objects.get(RegistID=R_ID).company,
                            by_U_ID=request.user.U_ID,
                        )
                        n += 1
                    contexts["Interviewers_count"] = n
            return render(request, "main/regist/regist_done.html", contexts)
        else:
            pass

    contexts["C_Form"] = C_Form

    contexts["D_Form"] = D_Form

    contexts["A_Form"] = A_Form

    contexts["I_Form"] = I_Form

    contexts["M_Form"] = M_Form

    contexts["AD_Form"] = AD_Form
    return render(request, "main/regist/regist_all.html", contexts)


@login_required
def mypage(request):
    contexts = collect_regnum(request)
    user = CustomUser.objects.get(username=request.user)
    contexts["user"] = user
    n_regist = RegistSets.objects.filter(by_U_ID=user.U_ID).count()
    contexts["n_regist"] = n_regist
    n_interview = Interview.objects.filter(by_U_ID=user.U_ID).count()
    contexts["n_interview"] = n_interview
    contexts["regsets"] = collect_regsets(user)
    contexts["l_days"] = (user.ExpiryDate - dt.date.today()).days
    return render(request, "main/mypage/mypage.html", contexts)


@login_required
def view_my_post(request, id):
    contexts = {}
    try:
        contexts = getRegistForms(id, contexts, request)
    except RegistSets.DoesNotExist:
        return redirect(to="mypage")
    except AttributeError:
        return HttpResponse("<h3>アクセス権限がありません。ログイン情報を確かめるか、管理者に問い合わせてください</h3>")
    return render(request, "main/mypage/view_my_post.html", contexts)


@login_required
def delete_posts(request, id):
    contexts = getRegistForms(id, {}, request)
    if request.method == "POST":
        if "del_R_Set" in request.POST:
            post = RegistSets.objects.get(RegistID=id)
            if post.about is not None:
                post.about.delete()
            if post.idea is not None:
                post.idea.delete()
            if post.motivation is not None:
                post.motivation.delete()
            if post.d_company is not None:
                post.d_company.delete()
            if post.adoption is not None:
                post.adoption.delete()
            post.delete()
        elif "del_C_Form" in request.POST:
            try:
                post = Companies.objects.get(
                    CompanyID=RegistSets.objects.get(RegistID=id).company.CompanyID
                )
                post.delete()
                RegistSets.objects.get(RegistID=id).delete()
            except Companies.DoesNotExist:
                RegistSets.objects.get(RegistID=id).delete()
        else:
            post = RegistSets.objects.get(RegistID=id)
            if "del_A_Form" in request.POST:
                post.about.delete()
            if "del_I_Form" in request.POST:
                post.idea.delete()
            if "del_M_Form" in request.POST:
                post.motivation.delete()
            if "del_D_Form" in request.POST:
                post.d_company.delete()
            if "del_AD_Form" in request.POST:
                post.adoption.delete()
        return HttpResponse(
            f"削除しています...<script>window.opener.location.href='{reverse('mypage')}'</script>"
        )
    return render(request, "main/mypage/delete.html", contexts)


@login_required
def regist_sets(request):
    contexts = collect_regnum(request)
    return render(request, "main/regist/sets/main.html", contexts)


@login_required
def create_company(request):
    contexts = collect_regnum(request)
    if request.method == "POST":
        C_Form = CompaniesForm(request.POST)
        if C_Form.is_valid():
            CompanyID = secrets.token_hex(64)
            n_CForm = C_Form.save(commit=False)
            n_CForm.CompanyID = CompanyID
            n_CForm.by_U_ID = request.user.U_ID
            n_CForm.save()
            Temp_regist = RegistSets.objects.create(
                RegistID=secrets.token_hex(64),
                by_U_ID=request.user.U_ID,
                company=Companies.objects.get(CompanyID=CompanyID),
            )
            request.session["RegistID"] = Temp_regist.RegistID
            print("RegistSets is created.")
            return redirect("create_about")
    C_Form = CompaniesForm()
    if "forms" in request.session:
        C_Form = CompaniesForm(request.session["forms"]["C_Form"])
    contexts["C_Form"] = C_Form
    return render(request, "main/regist/sets/create_company.html", contexts)


@login_required
def import_company(request):
    contexts = collect_regnum(request)
    if request.method == "POST":
        if "import" in request.POST:
            copy_company = Companies.objects.get(CompanyID=request.POST["ID"])
            CompanyID = request.POST["ID"]
            copy_company.CompanyID = CompanyID
            copy_company.by_U_ID = request.user.U_ID
            copy_company.save()
            Temp_regist = RegistSets.objects.create(
                RegistID=secrets.token_hex(64),
                by_U_ID=request.user.U_ID,
                company=Companies.objects.get(CompanyID=CompanyID),
            )
            print("RegistSets is created.")
            request.session["RegistID"] = Temp_regist.RegistID
            return redirect("create_about")
    companies = Companies.objects.filter(by_U_ID=request.user.U_ID).all()
    contexts["posts"] = companies
    return render(request, "main/regist/sets/import_company.html", contexts)


@login_required
def create_about(request):
    contexts = collect_regnum(request)
    A_Form = AboutForm()
    if "forms" in request.session:
        A_Form = AboutForm(request.session["forms"]["A_Form"])
    contexts["A_Form"] = A_Form
    contexts["C_Form"] = CompaniesForm(
        instance=RegistSets.objects.get(RegistID=request.session["RegistID"], by_U_ID=request.user.U_ID).company
    )
    if request.method == "POST":
        A_Form = AboutForm(request.POST)
        if A_Form.is_valid():
            n_AForm = A_Form.save(commit=False)
            n_AForm.company_name = RegistSets.objects.get(
                RegistID=request.session["RegistID"], by_U_ID=request.user.U_ID
            ).company
            AboutID = secrets.token_hex(64)
            n_AForm.AboutID = AboutID
            n_AForm.by_U_ID = request.user.U_ID
            n_AForm.save()
            Temp_regist = RegistSets.objects.get(RegistID=request.session["RegistID"], by_U_ID=request.user.U_ID)
            Temp_regist.about = About.objects.get(AboutID=AboutID, by_U_ID=request.user.U_ID)
            Temp_regist.save()
            return redirect("create_idea")

    return render(request, "main/regist/sets/create_about.html", contexts)


@login_required
def create_idea(request):
    contexts = collect_regnum(request)
    contexts["A_Form"] = AboutForm(
        instance=RegistSets.objects.get(RegistID=request.session["RegistID"], by_U_ID=request.user.U_ID).about
    )
    I_Form = IdeaForm()
    contexts["I_Form"] = I_Form
    if request.method == "POST":
        I_Form = IdeaForm(request.POST)
        if I_Form.is_valid():
            n_IForm = I_Form.save(commit=False)
            n_IForm.company_name = RegistSets.objects.get(
                RegistID=request.session["RegistID"], by_U_ID=request.user.U_ID
            ).company
            IdeaID = secrets.token_hex(64)
            n_IForm.IdeaID = IdeaID
            n_IForm.by_U_ID = request.user.U_ID
            n_IForm.save()
            Temp_regist = RegistSets.objects.get(RegistID=request.session["RegistID"], by_U_ID=request.user.U_ID)
            Temp_regist.idea = Idea.objects.get(IdeaID=IdeaID, by_U_ID=request.user.U_ID)
            Temp_regist.save()
            return redirect("create_motivation")
    return render(request, "main/regist/sets/create_idea.html", contexts)


@login_required
def create_motivation(request):
    contexts = collect_regnum(request)
    contexts["I_Form"] = IdeaForm(
        instance=RegistSets.objects.get(RegistID=request.session["RegistID"], by_U_ID=request.user.U_ID).idea
    )
    M_Form = MotivationForm()
    contexts["M_Form"] = M_Form
    if request.method == "POST":
        M_Form = MotivationForm(request.POST)
        if M_Form.is_valid():
            n_MForm = M_Form.save(commit=False)
            n_MForm.company_name = RegistSets.objects.get(
                RegistID=request.session["RegistID"], by_U_ID=request.user.U_ID
            ).company
            MotivationID = secrets.token_hex(64)
            n_MForm.MotivationID = MotivationID
            n_MForm.by_U_ID = request.user.U_ID
            n_MForm.save()
            Temp_regist = RegistSets.objects.get(RegistID=request.session["RegistID"], by_U_ID=request.user.U_ID)
            Temp_regist.motivation = Motivation.objects.get(MotivationID=MotivationID, by_U_ID=request.user.U_ID)
            Temp_regist.save()
            return redirect("create_d_company")
    return render(request, "main/regist/sets/create_motivation.html", contexts)


@login_required
def create_d_company(request):
    contexts = collect_regnum(request)
    contexts["M_Form"] = MotivationForm(
        instance=RegistSets.objects.get(RegistID=request.session["RegistID"], by_U_ID=request.user.U_ID).motivation
    )
    D_Form = D_CompanyForm()
    if "forms" in request.session:
        D_Form = D_CompanyForm(request.session["forms"]["D_Form"])
    contexts["D_Form"] = D_Form
    if request.method == "POST":
        D_Form = D_CompanyForm(request.POST)
        if D_Form.is_valid():
            n_DForm = D_Form.save(commit=False)
            n_DForm.company_name = RegistSets.objects.get(
                RegistID=request.session["RegistID"], by_U_ID=request.user.U_ID
            ).company
            D_CompanyID = secrets.token_hex(64)
            n_DForm.D_CompanyID = D_CompanyID
            n_DForm.by_U_ID = request.user.U_ID
            n_DForm.save()
            Temp_regist = RegistSets.objects.get(RegistID=request.session["RegistID"], by_U_ID=request.user.U_ID)
            Temp_regist.d_company = D_Company.objects.get(D_CompanyID=D_CompanyID, by_U_ID=request.user.U_ID)
            Temp_regist.save()
            return redirect("create_adoption")
    return render(request, "main/regist/sets/create_d_company.html", contexts)


@login_required
def create_adoption(request):
    contexts = collect_regnum(request)
    contexts["D_Form"] = D_CompanyForm(
        instance=RegistSets.objects.get(RegistID=request.session["RegistID"], by_U_ID=request.user.U_ID).d_company
    )
    AD_Form = AdoptionForm()
    contexts["AD_Form"] = AD_Form
    if request.method == "POST":
        AD_Form = AdoptionForm(request.POST)
        if AD_Form.is_valid():
            n_ADForm = AD_Form.save(commit=False)
            n_ADForm.company_name = RegistSets.objects.get(
                RegistID=request.session["RegistID"], by_U_ID=request.user.U_ID
            ).company
            AdoptionID = secrets.token_hex(64)
            n_ADForm.AdoptionID = AdoptionID
            n_ADForm.by_U_ID = request.user.U_ID
            n_ADForm.save()
            Temp_regist = RegistSets.objects.get(RegistID=request.session["RegistID"], by_U_ID=request.user.U_ID)
            Temp_regist.adoption = Adoption.objects.get(AdoptionID=AdoptionID, by_U_ID=request.user.U_ID)
            Temp_regist.save()
            return redirect("create_complete")
    return render(request, "main/regist/sets/create_adoption.html", contexts)


@login_required
def create_complete(request):
    contexts = collect_regnum(request)
    regist = RegistSets.objects.get(RegistID=request.session["RegistID"])
    del request.session["RegistID"]
    contexts["C_Form"] = CompaniesForm(instance=regist.company)
    contexts["A_Form"] = AboutForm(instance=regist.about)
    contexts["I_Form"] = IdeaForm(instance=regist.idea)
    contexts["M_Form"] = MotivationForm(instance=regist.motivation)
    contexts["D_Form"] = D_CompanyForm(instance=regist.d_company)
    contexts["AD_Form"] = AdoptionForm(instance=regist.adoption)
    return render(request, "main/regist/sets/create_complete.html", contexts)


@login_required
def edit_posts(request, id):
    if request.method == "GET":
        try:
            contexts = getRegistForms(id, collect_regnum(request), request)
        except (RegistSets.DoesNotExist, AttributeError):
            return HttpResponse("<h4>権限がない、もしくは不正なアクセスです。</h4><button onclick='window.location=`/`'>戻る</button>")
        if contexts["as_staff"] is True:
            return HttpResponse("<h3>管理者は、ユーザーの登録情報シートに変更を加えることができません</h3><button onclick='window.location=`/`'>戻る</button>")
        NotFound = []
        contexts["R_id"] = id
        if "A_Form" not in contexts:
            contexts["A_Form"] = AboutForm()
            NotFound.append("A_Form")
        if "I_Form" not in contexts:
            contexts["I_Form"] = IdeaForm()
            NotFound.append("I_Form")
        if "M_Form" not in contexts:
            contexts["M_Form"] = MotivationForm()
            NotFound.append("M_Form")
        if "D_Form" not in contexts:
            contexts["D_Form"] = D_CompanyForm()
            NotFound.append("D_Form")
        if "AD_Form" not in contexts:
            contexts["AD_Form"] = AdoptionForm()
            NotFound.append("AD_Form")
        request.session["NotFound"] = NotFound

    if request.method == "POST":
        res = {"status": "", "message": ""}
        try:
            Temp_regist = RegistSets.objects.get(RegistID=id, by_U_ID=request.user.U_ID)
        except (RegistSets.DoesNotExist, AttributeError):
            res["status"] = "NG"
            res["message"] = "不正な操作を検出しました。操作を取り消しました。管理者までお問い合わせください。"
            return JsonResponse(res)
        if "A_Form" in request.session["NotFound"]:
            AboutID = secrets.token_hex(64)
            A_Form = AboutForm(request.POST)
        else:
            A_Form = AboutForm(request.POST, instance=Temp_regist.about)
            AboutID = Temp_regist.about.AboutID
        if "I_Form" in request.session["NotFound"]:
            I_Form = IdeaForm(request.POST)
            IdeaID = secrets.token_hex(64)
        else:
            I_Form = IdeaForm(request.POST, instance=Temp_regist.idea)
            IdeaID = Temp_regist.idea.IdeaID
        if "M_Form" in request.session["NotFound"]:
            MotivationID = secrets.token_hex(64)
            M_Form = MotivationForm(request.POST)
        else:
            M_Form = MotivationForm(request.POST, instance=Temp_regist.motivation)
            MotivationID = Temp_regist.motivation.MotivationID
        if "D_Form" in request.session["NotFound"]:
            D_CompanyID = secrets.token_hex(64)
            D_Form = D_CompanyForm(request.POST)
        else:
            D_Form = D_CompanyForm(request.POST, instance=Temp_regist.d_company)
            D_CompanyID = Temp_regist.d_company.D_CompanyID
        if "AD_Form" in request.session["NotFound"]:
            AdoptionID = secrets.token_hex(64)
            AD_Form = AdoptionForm(request.POST)
        else:
            AD_Form = AdoptionForm(request.POST, instance=Temp_regist.adoption)
            AdoptionID = Temp_regist.adoption.AdoptionID
        if (A_Form.is_valid() and I_Form.is_valid() and M_Form.is_valid() and D_Form.is_valid() and AD_Form.is_valid()):
            n_AForm = A_Form.save(commit=False)
            n_IForm = I_Form.save(commit=False)
            n_MForm = M_Form.save(commit=False)
            n_DForm = D_Form.save(commit=False)
            n_ADForm = AD_Form.save(commit=False)

            n_AForm.AboutID = AboutID
            n_IForm.IdeaID = IdeaID
            n_MForm.MotivationID = MotivationID
            n_DForm.D_CompanyID = D_CompanyID
            n_ADForm.AdoptionID = AdoptionID
            n_AForm.company_name = Temp_regist.company
            n_IForm.company_name = Temp_regist.company
            n_MForm.company_name = Temp_regist.company
            n_DForm.company_name = Temp_regist.company
            n_ADForm.company_name = Temp_regist.company
            n_AForm.by_U_ID = request.user.U_ID
            n_IForm.by_U_ID = request.user.U_ID
            n_MForm.by_U_ID = request.user.U_ID
            n_DForm.by_U_ID = request.user.U_ID
            n_ADForm.by_U_ID = request.user.U_ID
            n_AForm.save()
            n_IForm.save()
            n_MForm.save()
            n_DForm.save()
            n_ADForm.save()
            Temp_regist.about = About.objects.get(AboutID=AboutID, by_U_ID=request.user.U_ID)
            Temp_regist.idea = Idea.objects.get(IdeaID=IdeaID, by_U_ID=request.user.U_ID)
            Temp_regist.motivation = Motivation.objects.get(MotivationID=MotivationID, by_U_ID=request.user.U_ID)
            Temp_regist.d_company = D_Company.objects.get(D_CompanyID=D_CompanyID, by_U_ID=request.user.U_ID)
            Temp_regist.adoption = Adoption.objects.get(AdoptionID=AdoptionID, by_U_ID=request.user.U_ID)
            Temp_regist.save()
            res["status"] = "OK"
        else:
            res["status"] = "ERROR"
            for f in [A_Form.errors, I_Form.errors, M_Form.errors, D_Form.errors, AD_Form.errors]:
                res["message"] += str(f) + "<br>"
        return JsonResponse(res)
    return render(request, "main/mypage/edit_posts.html", contexts)


@login_required
def search_company(request, return_to):
    contexts = collect_regnum(request)
    contexts["return_to"] = return_to
    form = SearchForm_corpnum()
    if request.user.gBIZINFO_key == "default_key":
        return HttpResponse(
            r"GBIZINFO_key is not set. Please set your key in your profile. <a href='/'>Profile</a>"
        )
    if request.method == "POST":
        if "search" in request.POST:
            form = SearchForm_corpnum(request.POST)
            if form.is_valid():
                url = "https://info.gbiz.go.jp/hojin/v1/hojin?"
                if form.cleaned_data["prefecture"] != "00":
                    url += "&prefecture=" + form.cleaned_data["prefecture"]
                if form.cleaned_data["corporate_number"] != "":
                    url += "&corporate_number" + form.cleaned_data["corporate_number"]
                if form.cleaned_data["name"] != "":
                    url += "&name=" + quote(form.cleaned_data["name"])
                if (form.cleaned_data["city"] != "000"):
                    url += "&city=" + form.cleaned_data["city"]
                if form.cleaned_data["founded_year"] is not None:
                    url += "&founded_year=" + str(form.cleaned_data["founded_year"])
                headers = {
                    "Accept": "application/json",
                    "X-hojinInfo-api-token": request.user.gBIZINFO_key,
                }
                if url != "https://info.gbiz.go.jp/hojin/v1/hojin?":
                    try:
                        r = requests.get(url, headers=headers)
                        contexts["results"] = r.json()["hojin-infos"]
                    except requests.exceptions.ConnectionError:
                        contexts["results"] = []
                        contexts["message"] = ("情報を取得できませんでした。ネットワーク接続、ファイアウォールの設定を確認し、再度お試しください。")
                    except KeyError:
                        contexts["results"] = []
                        if r.status_code == 401:
                            contexts["message"] = (f" APIキーが不正です。管理者にご連絡ください。(code: {r.status_code})")
                        else:
                            contexts["message"] = (f"条件に一致する検索結果がありませんでした。再度確認してください (code: {r.status_code})")
    contexts["form"] = form
    return render(request, "main/regist/sets/search_company.html", contexts)


@login_required
def get_city(request, prefecture):
    res = {}
    with open("static/assets/address_code.csv", "r", encoding="utf-8-sig") as f:
        lst = csv.DictReader(f)
        for row in lst:
            if row["code"][:2:] == prefecture:
                res[row['city']] = {"code": row["code"][2:5:], "yomi": row["city_y"]}
        res = dict(sorted(res.items(), key=lambda x: x[1]["yomi"]))
    return JsonResponse(res)


@login_required
def get_more_compinfo(request, corporate_number, return_to):
    contexts = collect_regnum(request)
    contexts["return_to"] = return_to
    if request.user.gBIZINFO_key == "default_key":
        return HttpResponse(
            "GBIZINFO_key is not set. Please set your key in your profile. <a href='{{url 'mypage'}}'>Profile</a>"
        )
    headers = {
        "Accept": "application/json",
        "X-hojinInfo-api-token": request.user.gBIZINFO_key,
    }
    url = "https://info.gbiz.go.jp/hojin/v1/hojin/" + corporate_number
    try:
        contexts["result"] = requests.get(url, headers=headers).json()["hojin-infos"][0]
    except requests.ConnectionError:
        return HttpResponse("データの取得に失敗しました。ネットワークの接続を確認してください")
    return render(request, "main/regist/sets/get_more_compinfo.html", contexts)


@login_required
def set_searched_data(request):
    if request.method == "POST":
        return_to = "regist_all" if request.POST["return_to"] == "regist_all" else "index"
        corporate_number = request.POST["corporate_number"]
        url = "https://info.gbiz.go.jp/hojin/v1/hojin/" + corporate_number
        headers = {
            "Accept": "application/json",
            "X-hojinInfo-api-token": request.user.gBIZINFO_key,
        }
        try:
            res = requests.get(url, headers=headers).json()["hojin-infos"][0]
        except requests.ConnectionError:
            return HttpResponse("データの取得に失敗しました。ネットワークの接続を確認してください")
        C = {
            "name": res["name"] if "name" in res else "None",
            "industry": (
                res["business_summary"] if "business_summary" in res else "None"
            ),
            "president": (
                res["representative_position"]
                if "representative_position" in res
                else ""
            )
            + (res["representative_name"] if "representative_name" in res else ""),
            "Ca_year": "0",
            "contact": "-",
        }

        A = {
            "product": res["business_summary"] if "business_summary" in res else "None",
            "customer_txt": "-",
            "customer": "B to B",
            "value_txt": "-",
            "value": "B to B",
            "originality": "-",
            "f_value": "-",
        }

        D = {
            "founded": (
                res["date_of_establishment"] if "date_of_establishment" in res else "0"
            ),
            "founded_t": "なし",
            "capital": (
                res["capital_stock_summary_of_business_results"]
                if "capital_stock_summary_of_business_results" in res
                else 0
            ),
            "sales_n": (
                res["net_sales_summary_of_business_results "]
                if "net_sales_summary_of_business_results " in res
                else 0
            ),
            "employee_n": res["employee_number "] if "employee_number " in res else 0,
            "sales_y": datetime.strptime(res["update_date"][:10:], r"%Y-%m-%d").year if "update_date" in res else 0,
            "sales_t": "なし",
            "employee_t": "なし",
            "stock_t": "なし",
            "t_p": 0,
            "avg_y": res["average_age "] if "average_age " in res else 0,
            "postal_code": res["postal_code"] if "postal_code" in res else 0,
            "location": res["location"] if "location" in res else "なし",
            "corporate_number": (
                res["corporate_number"] if "corporate_number" in res else 0
            ),
            "url": res["company_url"] if "company_url" in res else "about:blank",
        }

        request.session["forms"] = {
            "C_Form": C,
            "A_Form": A,
            "D_Form": D,
        }
        return redirect(return_to)


@login_required
def interview_main(request, id):
    contexts = collect_regnum(request)
    try:
        R_sets = RegistSets.objects.get(RegistID=id, by_U_ID=request.user.U_ID)
        interviews = Interview.objects.filter(RegistID=R_sets, by_U_ID=request.user.U_ID).order_by("date")
        contexts["as_staff"] = False
    except RegistSets.DoesNotExist:
        if request.user.is_staff:
            R_sets = RegistSets.objects.get(RegistID=id)
            interviews = Interview.objects.filter(RegistID=R_sets).order_by("date")
            contexts["as_staff"] = True
        else:
            return HttpResponse("存在しない登録情報シート、もしくは閲覧権限がありません。")
    contexts["R_sets"] = R_sets
    contexts["interviews"] = interviews
    return render(request, "main/interview/interview_main.html", contexts)


@login_required
def interview_create(request, id):
    contexts = collect_regnum(request)
    form = InterviewForm(initial={"RegistID": id, "InterviewID": secrets.token_hex(64), "date": timezone.now()})
    name = RegistSets.objects.get(RegistID=id, by_U_ID=request.user.U_ID).company.name
    contexts["form"] = form
    contexts["name"] = name
    contexts["R_id"] = id
    if request.method == "POST":
        form = InterviewForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.company_name = name
            data.by_U_ID = request.user.U_ID
            data.save()
            return redirect("interview_main", id)
        else:
            contexts["errors"] = form.errors.as_text()
            contexts["form"] = form
    return render(request, "main/interview/interview_create.html", contexts)


@login_required
def delete_interview(request, id):
    try:
        Interview.objects.get(InterviewID=id, by_U_ID=request.user.U_ID).delete()
    except Interview.DoesNotExist:
        if request.user.is_staff:
            return HttpResponse("管理者は面談録の削除を行うことができません")
        return HttpResponse("削除に失敗しました。権限がない、もしくは存在しない面談録です")
    return HttpResponse("削除しました この画面を閉じてください")


@login_required
def get_address(request, zipcode):
    contexts = {}
    url = r"https://zipcloud.ibsnet.co.jp/api/search?zipcode=" + zipcode
    try:
        res = requests.get(url).json()
        if res["status"] != 200 or res["results"] is None:
            contexts["message"] = {"color": "warning", "message": f"結果が存在しません。再度確認してください   (レスポンス: {res['message'] if res['message'] is not None else 'NotFound'})"}
    except ConnectionError:
        contexts["message"] = {"color": "danger", "message": "ネットワークエラーが発生しました。接続とファイアウォールの設定を確認してください"}
    contexts["res"] = res["results"]
    return render(request, "main/interview/get_address.html", contexts)


@login_required
def view_interview(request, id):
    try:
        contexts = collect_regnum(request)
        try:
            inst = Interview.objects.get(InterviewID=id, by_U_ID=request.user.U_ID)
            contexts["as_staff"] = False
        except (Interview.DoesNotExist, AttributeError):
            if request.user.is_staff:  # すべてのユーザーの面談録の閲覧が可能
                contexts["as_staff"] = True
                inst = Interview.objects.get(InterviewID=id)
            else:
                return HttpResponse("アクセス権限がありません。操作は取り消されました。アカウントを確認するか、管理者に連絡してください")
        interview = InterviewForm(instance=inst)
        contexts["interview"] = interview
        contexts["inst"] = inst
        contexts["RegistID"] = inst.RegistID.RegistID
        try:
            contexts["from_url"] = inst.RegistID.adoption.from_url
        except AttributeError:
            contexts["from_url"] = None
        if request.method == "POST":
            res = {}
            form = InterviewForm(
                request.POST, instance=Interview.objects.get(InterviewID=id, by_U_ID=request.user.U_ID)
            )
            if form.is_valid():
                form.save()
                res["is_saved"] = True
                res["saved_time"] = timezone.now().astimezone().time()
            else:
                res["is_saved"] = False
                res["errors"] = str(form.errors)
            return JsonResponse(res)
        return render(request, "main/interview/view_interview.html", contexts)
    except Interview.DoesNotExist:
        contexts["is_saved"] = False
        return HttpResponse(" <script>window.close()</script> ")


@login_required
def calc(request):
    contexts = {}
    return render(request, "main/regist/calc.html", contexts)


@login_required
def export_sheet(request, id):
    contexts = {}
    if request.method == "POST":
        try:
            R_set = RegistSets.objects.get(RegistID=id, by_U_ID=request.user.U_ID)
            C = dict(**{"sheet_name": "Company"}, **model_to_dict(R_set.company))
            del C["CompanyID"]
            A = dict(**{"sheet_name": "About"}, **model_to_dict(R_set.about))
            del A["AboutID"]
            Id = dict(**{"sheet_name": "Idea"}, **model_to_dict(R_set.idea))
            del Id["IdeaID"]
            M = dict(**{"sheet_name": "Motivation"}, **model_to_dict(R_set.motivation))
            del M["MotivationID"]
            D = dict(**{"sheet_name": "D_company"}, **model_to_dict(R_set.d_company))
            del D["D_CompanyID"]
            AD = dict(**{"sheet_name": "Adoption"}, **model_to_dict(R_set.adoption))
            del AD["AdoptionID"]
            sets = {
                "Company": C,
                "About": A,
                "Idea": Id,
                "Motivation": M,
                "D_Company": D,
                "Adoption": AD,
            }
            name = R_set.company.name
        except AttributeError:
            return HttpResponse("エラーが発生しました<br>欠落しているシートが存在しています。詳細はお問い合わせください。<br>")

        if request.POST["data"] == "two" or request.POST["data"] == "three":
            name += "_include_interview"
            interviews = Interview.objects.filter(RegistID=id, by_U_ID=request.user.U_ID)
            sets["Interview"] = {
                "sheet_name": "Interviews",
                "interviews": [model_to_dict(interview, exclude=["ESlist"]) for interview in interviews],
            }
            for s in sets["Interview"]["interviews"]:
                if isinstance(s["date"], datetime):
                    s["date"] = s["date"].isoformat()
                del s["id"]
                del s["RegistID"]
                del s["InterviewID"]
                del s["by_U_ID"]
            if request.POST["data"] == "three":
                name += "_include_interviewer"
                interviewers = Interviewer.objects.filter(by_U_ID=request.user.U_ID, company_name=R_set.company)
                if interviewers.count() > 0:
                    sets["Interviewer"] = {
                        "sheet_name": "Interviewers",
                        "interviewers": [model_to_dict(interviewer) for interviewer in interviewers],
                    }
                    for s in sets["Interviewer"]["interviewers"]:
                        del s["id"]
                        del s["by_U_ID"]
                        del s["company_name"]
        for s in sets.values():
            if "_state" in s:
                del s["_state"]
            if "company_name" in s:
                del s["company_name"]
            if "by_U_ID" in s:
                del s["by_U_ID"]
        name += "_exported_sheet"
        try:
            if request.POST["type"] == "csv":
                response = HttpResponse(content_type="text/csv; charset=shift-jis")
                for s in sets.values():
                    csv_columns = list(s.keys())
                    writer = csv.DictWriter(response, csv_columns)
                    writer.writeheader()
                    writer.writerow(s)
                    writer.writerow({})
                response["Content-Disposition"] = "attachment; filename*=UTF-8''{}".format(
                    urllib.parse.quote((f"{name}.csv").encode("utf8"))
                )
                return response
        except UnicodeEncodeError:
            return HttpResponse("エラーが発生しました<br>環境依存文字が使用されている可能性があります。管理者までお問い合わせください<br>")
        else:

            class DateTimeEncoder(json.JSONEncoder):
                def default(self, obj):
                    if isinstance(obj, datetime):
                        return obj.isoformat()
                    return super(DateTimeEncoder, self).default(obj)

            response = HttpResponse(content_type="application/json")
            if request.POST["type"] == "json_asF":
                response["Content-Disposition"] = (
                    "attachment; filename*=UTF-8''{}".format(
                        urllib.parse.quote((f"{name}.json").encode("utf8"))
                    )
                )
            response.write(json.dumps(sets, cls=DateTimeEncoder, ensure_ascii=False))
            return response
    contexts["conpany_name"] = RegistSets.objects.get(RegistID=id, by_U_ID=request.user.U_ID).company.name
    return render(request, "main/mypage/export_sheet.html", contexts)


@login_required
def json_import(request):
    contexts = {}
    if request.method == "POST":
        try:
            file = request.FILES["json"]
            data = json.load(file)
            request.session["jsons"] = {
                "C_Form": data["Company"],
                "A_Form": data["About"],
                "I_Form": data["Idea"],
                "M_Form": data["Motivation"],
                "D_Form": data["D_Company"],
                "AD_Form": data["Adoption"],
            }
            request.session["Interviews"] = (
                data["Interview"] if "Interview" in data else "None"
            )
            request.session["Interviewers"] = (
                data["Interviewer"] if "Interviewer" in data else "None"
            )
            return HttpResponse("<script>window.opener.location.reload();</script>")
        except (KeyError, UnicodeDecodeError):
            contexts["message"] = "インポートに失敗しました。ファイルを確かめて再度実行するか、手入力にて登録してください "
    return render(request, "main/regist/sets/json_import.html", contexts)


@login_required
def change_active(request):
    if request.method == "POST":
        RegistSets.objects.filter(RegistID=request.POST.get("RegistID"), by_U_ID=request.user.U_ID).update(
            isActive=(True if request.POST.get("current_status") != "True" else False)
        )
    return HttpResponse("<script>window.opener.location.reload()</script>")


@login_required
def get_interviewer(request, id):
    try:
        interviewer = RegistSets.objects.get(RegistID=id, by_U_ID=request.user.U_ID).company.contact
        return JsonResponse({"status": "OK", "interviewer": interviewer})
    except (RegistSets.DoesNotExist, AttributeError):
        return JsonResponse({"status": "NG", "res": "不正なリクエストです。処理は中断されました。管理者まで問い合わせてください。"})


@login_required
def prof_interviewer(request, company_id, i_name):
    if request.method == "GET":
        contexts = collect_regnum(request)
        try:
            company = RegistSets.objects.filter(by_U_ID=request.user.U_ID).get(company=company_id).company
            contexts["as_staff"] = False
        except (RegistSets.DoesNotExist, AttributeError):
            if request.user.is_staff:
                try:
                    company = RegistSets.objects.get(company=company_id).company
                    contexts["as_staff"] = True
                except (RegistSets.DoesNotExist, AttributeError):
                    return HttpResponse("データが存在しません。")
            else:
                return HttpResponse("不正なリクエストです")
        contexts["company"] = company.name
        contexts["company_id"] = company_id
        contexts["i_name"] = i_name
        try:
            if contexts["as_staff"] is False:
                instance_data = Interviewer.objects.get(
                    by_U_ID=request.user.U_ID,
                    company_name=company,
                    name=i_name,
                )
            elif contexts["as_staff"] is True:
                try:
                    instance_data = Interviewer.objects.get(
                        company_name=company,
                        name=i_name,
                    )
                except Interviewer.DoesNotExist:
                    return HttpResponse("面談者情報が存在しません。登録を確認してください")
            else:
                return HttpResponse("不正なリクエストです")
            init_form = Form_Prof_Interviewer(instance=instance_data)
            if contexts["as_staff"] is False:
                contexts["message"] = {"type": "success", "texts": ["一致した担当者情報があります", "編集して保存することができます"]}
            if contexts["as_staff"] is True:
                contexts["message"] = {"type": "info", "texts": ["一致した担当者情報があります", "管理者権限による閲覧のため、閲覧のみ可能です"]}
        except Interviewer.DoesNotExist:
            init_form = Form_Prof_Interviewer(initial={"company_name": Companies.objects.get(CompanyID=company_id, by_U_ID=request.user.U_ID), "interviewer_name": i_name})
            contexts["message"] = {"type": "warning", "texts": ["一致する担当者情報が見つかりませんでした。", "新規作成を行います。名前と企業を確認し、項目を埋めてください"]}

    if request.method == "POST":
        try:
            try:
                company = RegistSets.objects.filter(by_U_ID=request.user.U_ID).get(company=company_id).company
            except (RegistSets.DoesNotExist, AttributeError):
                return JsonResponse({"status": "NG", "reason": "不正なリクエストです。操作は取り消されました。管理者までお問い合わせください。"})
            data = Interviewer.objects.get(
                by_U_ID=request.user.U_ID,
                company_name=company,
                name=i_name,
            )
            form = Form_Prof_Interviewer(request.POST, instance=data)
            reason = "上書き保存を行いました"
        except Interviewer.DoesNotExist:
            form = Form_Prof_Interviewer(request.POST)
            reason = "新規登録を行いました。"
        if form.is_valid():
            data = form.save(commit=False)
            data.by_U_ID = request.user.U_ID
            data.company_name = company
            data.name = i_name
            data.save()
            return JsonResponse({"status": "OK", "reason": reason})
        else:
            return JsonResponse({"status": "ERROR", "reason": "無効なフォームです", "error_list": str(form.errors)})

    contexts["form"] = init_form
    return render(request, "main/regist/interviewer.html", contexts)


@login_required
def search_post(request, sheet_from, where):
    contexts = {}
    res = RegistSets.objects.filter(by_U_ID=request.user.U_ID).order_by("-isActive")
    if sheet_from == "企業名":
        res = res.filter(company__name__contains=where)
    if sheet_from == "所属業界名":
        res = res.filter(company__industry__contains=where)
    if sheet_from == "所在地":
        res = res.filter(d_company__location__contains=where)
    if sheet_from == "担当者名":
        res = res.filter(company__contact__contains=where)
    contexts["posts"] = res
    post_interviews = {}
    for post in res:
        i = Interview.objects.filter(RegistID=post).order_by("-date").first()
        post_interviews[post.RegistID] = i.InterviewID if i is not None else None
    contexts["post_interviews"] = post_interviews
    return render(request, "main/mypage/search_result.html", contexts)


@login_required
def get_address_from_sheet(request, R_id):
    try:
        location = RegistSets.objects.get(RegistID=R_id, by_U_ID=request.user.U_ID).d_company.location
        postal_code = RegistSets.objects.get(RegistID=R_id, by_U_ID=request.user.U_ID).d_company.postal_code
        return JsonResponse({"status": "OK", "location": location, "postal_code": postal_code})
    except (RegistSets.DoesNotExist, AttributeError):
        return JsonResponse({"status": "NG", "res": "不正なリクエストです。処理は中断されました。管理者まで問い合わせてください。"})


@login_required
def ESModelSelect(request, I_ID):
    contexts = collect_regnum(request)
    interview = Interview.objects.get(by_U_ID=request.user.U_ID, InterviewID=I_ID)
    ES_set = ESModel.objects.filter(by_U_ID=request.user.U_ID)
    if request.method == "POST":
        returned = json.loads(request.POST["selected_data"])
        selected = {"sets": [], "date": timezone.now().astimezone().date()}
        if "all_clear" in request.POST:
            interview.ESlist.clear()
            selected["message"] = "すべての選択が解除されました。"
        else:
            for data in returned:
                interview.ESlist.add(ES_set.get(ESModelID=data))
                selected["sets"].append(
                    {
                        "title": ES_set.get(ESModelID=data).title,
                        "tag": ES_set.get(ESModelID=data).tag,
                        "desc": ES_set.get(ESModelID=data).desc
                    }
                    )
            selected["message"] = "登録されました。選択された項目を面談メモに追記しました"
        interview.save()
        return JsonResponse(selected)
    contexts["selected_ES"] = interview.ESlist.all()
    NotSelectedES = ES_set
    for es in contexts["selected_ES"]:
        NotSelectedES = NotSelectedES.exclude(ESModelID=es.ESModelID)
    contexts["NotSelectedES"] = NotSelectedES
    contexts["I_ID"] = I_ID
    contexts["ES_set"] = ES_set
    return render(request, "main/interview/select_ESdata.html", contexts)


@login_required
def GetEsModelDetail(request, id):
    contexts = {}
    data = ESModel.objects.get(by_U_ID=request.user.U_ID, ESModelID=id)
    form = ESModelForm(initial={"title": data.title, "desc": data.desc, "tag": data.tag})
    contexts["form"] = form
    return render(request, "main/interview/ESdata_detail.html", contexts)