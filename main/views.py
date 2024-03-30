from django.shortcuts import render, redirect, HttpResponse
from .models import (
    Companies,
    About,
    RegistSets,
    Idea,
    Motivation,
    D_Company,
    Adoption,
    Interview,
    CustomSheet,
)
from authUser.models import CustomUser
from .forms import (
    CompaniesForm,
    AboutForm,
    IdeaForm,
    MotivationForm,
    D_CompanyForm,
    AdoptionForm,
    SearchForm_corpnum,
    InterviewForm,
)
import secrets, requests, csv, urllib, json
from urllib.parse import quote
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.forms.models import model_to_dict
from django.db.models import Max, Sum, Avg, Count
from django.apps import apps
from django.urls import reverse
from django.http import JsonResponse



# Functions


def collect_regnum(request):
    if request.user.is_authenticated:
        res = {
            "num_c": Companies.objects.count(),
            "num_a": RegistSets.objects.filter(isActive=True, by_U_ID=request.user.U_ID).count(),
        }
    else:
        res = {}
    return res


def collect_regsets(user):
    res = RegistSets.objects.filter(by_U_ID=user.U_ID)
    return res


def getRegistSets(RegistID, contexts):
    post = RegistSets.objects.get(RegistID=RegistID)
    contexts["post"] = post
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
    contexts = collect_regnum(request)
    return render(request, "main/index.html", contexts)


@login_required
def regist_base(request):
    contexts = collect_regnum(request)
    return render(request, "main/regist/regist_base.html", contexts)


def regist_all(request):
    contexts = collect_regnum(request)
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
            n_CForm.save()

            C_Data = Companies.objects.get(CompanyID=CompanyID)
            n_AForm = A_Form.save(commit=False)
            n_AForm.company_name = C_Data
            n_AForm.AboutID = secrets.token_hex(64)
            n_IForm = I_Form.save(commit=False)
            n_IForm.company_name = C_Data
            n_IForm.IdeaID = secrets.token_hex(64)
            n_MForm = M_Form.save(commit=False)
            n_MForm.company_name = C_Data
            n_MForm.MotivationID = secrets.token_hex(64)
            n_DForm = D_Form.save(commit=False)
            n_DForm.company_name = C_Data
            n_DForm.D_CompanyID = secrets.token_hex(64)
            n_ADForm = AD_Form.save(commit=False)
            n_ADForm.company_name = C_Data
            n_ADForm.AdoptionID = secrets.token_hex(64)

            n_AForm.save()
            n_IForm.save()
            n_MForm.save()
            n_DForm.save()
            n_ADForm.save()
            R_ID = secrets.token_hex(64)
            n_RegistSets = RegistSets.objects.create(
                RegistID=R_ID,
                by_U_ID=CustomUser.objects.get(username=request.user).U_ID,
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
                for i in request.session["Interviews"]["interviews"]:
                    Interview.objects.create(
                        **i,
                        RegistID=RegistSets.objects.get(RegistID=R_ID),
                        InterviewID=secrets.token_hex(64),
                    )
                    n += 1
                contexts["In_counts"] = n
            return render(request, "main/regist/regist_done.html", contexts)
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
        else:
            contexts["messages"] = {
                "color": "success",
                "message": "<h5>インポートが完了しました。内容が正しいか確認し、登録を行ってください。</h5><h5>なお、面談録は情報に含まれていませんでした。</h5>",
            }
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

    contexts["C_Form"] = C_Form

    contexts["D_Form"] = D_Form

    contexts["A_Form"] = A_Form

    contexts["I_Form"] = I_Form

    contexts["M_Form"] = M_Form

    contexts["AD_Form"] = AD_Form
    return render(request, "main/regist/regist_all.html", contexts)


def show_data(request):
    companies = Companies.objects.all()
    contexts = {
        "companies": companies,
    }
    return render(request, "main/show.html", contexts)


@login_required
def mypage(request):
    contexts = collect_regnum(request)
    user = CustomUser.objects.get(username=request.user)
    contexts["user"] = user
    n_regist = RegistSets.objects.filter(by_U_ID=user.U_ID).count()
    contexts["n_regist"] = n_regist
    contexts["regsets"] = collect_regsets(user)
    posts = RegistSets.objects.filter(by_U_ID=request.user.U_ID).order_by("-isActive")
    contexts["posts"] = posts
    return render(request, "main/mypage/mypage.html", contexts)


def view_my_post(request, id):
    contexts = {}
    try:
        contexts = getRegistSets(id, contexts)
    except RegistSets.DoesNotExist:
        return redirect(to="mypage")
    return render(request, "main/mypage/view_my_post.html", contexts)


def delete_posts(request, id):
    contexts = getRegistSets(id, {})
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
                print("del_A_Form")
                post.about.delete()
            if "del_I_Form" in request.POST:
                print("del_I_Form")
                post.idea.delete()
            if "del_M_Form" in request.POST:
                print("del_M_Form")
                post.motivation.delete()
            if "del_D_Form" in request.POST:
                print("del_D_Form")
                post.d_company.delete()
            if "del_AD_Form" in request.POST:
                print("del_AD_Form")
                post.adoption.delete()
        return HttpResponse(
            f"削除しています...<script>window.opener.location.href='{reverse('mypage')}'</script>"
        )
    return render(request, "main/mypage/delete.html", contexts)


def regist_sets(request):
    contexts = collect_regnum(request)
    return render(request, "main/regist/sets/main.html", contexts)


def create_company(request):
    contexts = collect_regnum(request)
    if request.method == "POST":
        C_Form = CompaniesForm(request.POST)
        if C_Form.is_valid():
            CompanyID = secrets.token_hex(64)
            n_CForm = C_Form.save(commit=False)
            n_CForm.CompanyID = CompanyID
            n_CForm.save()
            Temp_regist = RegistSets.objects.create(
                RegistID=secrets.token_hex(64),
                by_U_ID=CustomUser.objects.get(username=request.user),
                company=Companies.objects.get(CompanyID=CompanyID),
            )
            request.session["RegistID"] = Temp_regist.RegistID
            print("new company created.")
            return redirect("create_about")
    C_Form = CompaniesForm()
    if "forms" in request.session:
        C_Form = CompaniesForm(request.session["forms"]["C_Form"])
    contexts["C_Form"] = C_Form
    return render(request, "main/regist/sets/create_company.html", contexts)


def import_company(request):
    contexts = collect_regnum(request)
    if request.method == "POST":
        if "import" in request.POST:
            copy_company = Companies.objects.get(CompanyID=request.POST["ID"])
            CompanyID = request.POST["ID"]
            copy_company.CompanyID = CompanyID
            copy_company.save()
            Temp_regist = RegistSets.objects.create(
                RegistID=secrets.token_hex(64),
                by_U_ID=CustomUser.objects.get(username=request.user),
                company=Companies.objects.get(CompanyID=CompanyID),
            )
            request.session["RegistID"] = Temp_regist.RegistID
            return redirect("create_about")
    companies = Companies.objects.all()
    contexts["posts"] = companies
    return render(request, "main/regist/sets/import_company.html", contexts)


def create_about(request):
    contexts = collect_regnum(request)
    A_Form = AboutForm()
    if "forms" in request.session:
        A_Form = AboutForm(request.session["forms"]["A_Form"])
    contexts["A_Form"] = A_Form
    contexts["C_Form"] = CompaniesForm(
        instance=RegistSets.objects.get(RegistID=request.session["RegistID"]).company
    )
    if request.method == "POST":
        A_Form = AboutForm(request.POST)
        if A_Form.is_valid():
            n_AForm = A_Form.save(commit=False)
            n_AForm.company_name = RegistSets.objects.get(
                RegistID=request.session["RegistID"]
            ).company
            AboutID = secrets.token_hex(64)
            n_AForm.AboutID = AboutID
            n_AForm.save()
            Temp_regist = RegistSets.objects.get(RegistID=request.session["RegistID"])
            Temp_regist.about = About.objects.get(AboutID=AboutID)
            Temp_regist.save()
            return redirect("create_idea")

    return render(request, "main/regist/sets/create_about.html", contexts)


def create_idea(request):
    contexts = collect_regnum(request)
    contexts["A_Form"] = AboutForm(
        instance=RegistSets.objects.get(RegistID=request.session["RegistID"]).about
    )
    I_Form = IdeaForm()
    contexts["I_Form"] = I_Form
    if request.method == "POST":
        I_Form = IdeaForm(request.POST)
        if I_Form.is_valid():
            n_IForm = I_Form.save(commit=False)
            n_IForm.company_name = RegistSets.objects.get(
                RegistID=request.session["RegistID"]
            ).company
            IdeaID = secrets.token_hex(64)
            n_IForm.IdeaID = IdeaID
            n_IForm.save()
            Temp_regist = RegistSets.objects.get(RegistID=request.session["RegistID"])
            Temp_regist.idea = Idea.objects.get(IdeaID=IdeaID)
            Temp_regist.save()
            return redirect("create_motivation")
    return render(request, "main/regist/sets/create_idea.html", contexts)


def create_motivation(request):
    contexts = collect_regnum(request)
    contexts["I_Form"] = IdeaForm(
        instance=RegistSets.objects.get(RegistID=request.session["RegistID"]).idea
    )
    M_Form = MotivationForm()
    contexts["M_Form"] = M_Form
    if request.method == "POST":
        M_Form = MotivationForm(request.POST)
        if M_Form.is_valid():
            n_MForm = M_Form.save(commit=False)
            n_MForm.company_name = RegistSets.objects.get(
                RegistID=request.session["RegistID"]
            ).company
            MotivationID = secrets.token_hex(64)
            n_MForm.MotivationID = MotivationID
            n_MForm.save()
            Temp_regist = RegistSets.objects.get(RegistID=request.session["RegistID"])
            Temp_regist.motivation = Motivation.objects.get(MotivationID=MotivationID)
            Temp_regist.save()
            return redirect("create_d_company")
    return render(request, "main/regist/sets/create_motivation.html", contexts)


def create_d_company(request):
    contexts = collect_regnum(request)
    contexts["M_Form"] = MotivationForm(
        instance=RegistSets.objects.get(RegistID=request.session["RegistID"]).motivation
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
                RegistID=request.session["RegistID"]
            ).company
            D_CompanyID = secrets.token_hex(64)
            n_DForm.D_CompanyID = D_CompanyID
            n_DForm.save()
            Temp_regist = RegistSets.objects.get(RegistID=request.session["RegistID"])
            Temp_regist.d_company = D_Company.objects.get(D_CompanyID=D_CompanyID)
            Temp_regist.save()
            return redirect("create_adoption")
    return render(request, "main/regist/sets/create_d_company.html", contexts)


def create_adoption(request):
    contexts = collect_regnum(request)
    contexts["D_Form"] = D_CompanyForm(
        instance=RegistSets.objects.get(RegistID=request.session["RegistID"]).d_company
    )
    AD_Form = AdoptionForm()
    contexts["AD_Form"] = AD_Form
    if request.method == "POST":
        AD_Form = AdoptionForm(request.POST)
        if AD_Form.is_valid():
            n_ADForm = AD_Form.save(commit=False)
            n_ADForm.company_name = RegistSets.objects.get(
                RegistID=request.session["RegistID"]
            ).company
            AdoptionID = secrets.token_hex(64)
            n_ADForm.AdoptionID = AdoptionID
            n_ADForm.save()
            Temp_regist = RegistSets.objects.get(RegistID=request.session["RegistID"])
            Temp_regist.adoption = Adoption.objects.get(AdoptionID=AdoptionID)
            Temp_regist.save()
            return redirect("create_complete")
    return render(request, "main/regist/sets/create_adoption.html", contexts)


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


def edit_posts(request, id):
    contexts = getRegistSets(id, collect_regnum(request))
    NotFound = []
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
        Temp_regist = RegistSets.objects.get(RegistID=id)
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
        if (
            A_Form.is_valid()
            and I_Form.is_valid()
            and M_Form.is_valid()
            and D_Form.is_valid()
            and AD_Form.is_valid()
        ):
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
            n_AForm.save()
            n_IForm.save()
            n_MForm.save()
            n_DForm.save()
            n_ADForm.save()
            Temp_regist.about = About.objects.get(AboutID=AboutID)
            Temp_regist.idea = Idea.objects.get(IdeaID=IdeaID)
            Temp_regist.motivation = Motivation.objects.get(MotivationID=MotivationID)
            Temp_regist.d_company = D_Company.objects.get(D_CompanyID=D_CompanyID)
            Temp_regist.adoption = Adoption.objects.get(AdoptionID=AdoptionID)
            Temp_regist.save()
            return HttpResponse("<script>window.opener.location.reload()</script>")

    return render(request, "main/mypage/edit_posts.html", contexts)


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
                headers = {
                    "Accept": "application/json",
                    "X-hojinInfo-api-token": request.user.gBIZINFO_key,
                }
                if url != "https://info.gbiz.go.jp/hojin/v1/hojin?":
                    try:
                        r = requests.get(url, headers=headers)
                        print(r.status_code)
                        contexts["results"] = r.json()["hojin-infos"]
                    except KeyError:
                        contexts["results"] = []
                        contexts["message"] = (
                            f"条件に一致する検索結果がありませんでした。再度確認してください (code: {r.status_code})"
                        )
    contexts["form"] = form
    return render(request, "main/regist/sets/search_company.html", contexts)


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
    contexts["result"] = requests.get(url, headers=headers).json()["hojin-infos"][0]
    return render(request, "main/regist/sets/get_more_compinfo.html", contexts)


def set_searched_data(request):
    if request.method == "POST":
        return_to = request.POST["return_to"]
        corporate_number = request.POST["corporate_number"]
        url = "https://info.gbiz.go.jp/hojin/v1/hojin/" + corporate_number
        headers = {
            "Accept": "application/json",
            "X-hojinInfo-api-token": request.user.gBIZINFO_key,
        }
        res = requests.get(url, headers=headers).json()["hojin-infos"][0]
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
            "a_year": "0",
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
            "founded_t": "more100",
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
            "sales_y": res["update_date"] if "update_date" in res else 0,
            "sales_t": "None",
            "employee_t": "None",
            "stock_t": "None",
            "t_p": 0,
            "avg_y": res["average_age "] if "average_age " in res else 0,
            "postal_code": res["postal_code"] if "postal_code" in res else 0,
            "location": res["location"] if "location" in res else "None",
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


def interview_main(request, id):
    contexts = collect_regnum(request)
    R_sets = RegistSets.objects.get(RegistID=id)
    interviews = Interview.objects.filter(RegistID=R_sets)
    contexts["R_sets"] = R_sets
    contexts["interviews"] = interviews
    return render(request, "main/interview/interview_main.html", contexts)


def interview_create(request, id):
    contexts = collect_regnum(request)
    form = InterviewForm(initial={"RegistID": id, "InterviewID": secrets.token_hex(64)})
    name = RegistSets.objects.get(RegistID=id).company.name
    contexts["form"] = form
    contexts["name"] = name
    contexts["R_id"] = id
    if request.method == "POST":
        form = InterviewForm(request.POST)
        if form.is_valid():
            print("ok")
            data = form.save(commit=False)
            data.company_name = name
            data.save()
            return redirect("interview_main", id)
        else:
            print(form.errors.as_text())
            contexts["errors"] = form.errors.as_text()
            contexts["form"] = form
    return render(request, "main/interview/interview_create.html", contexts)


def get_address(request, zipcode):
    contexts = {}
    url = r"https://zipcloud.ibsnet.co.jp/api/search?zipcode=" + zipcode
    res = requests.get(url).json()["results"]
    contexts["res"] = res
    return render(request, "main/interview/get_address.html", contexts)


def view_interview(request, id):
    contexts = collect_regnum(request)
    interview = InterviewForm(instance=Interview.objects.get(InterviewID=id))
    contexts["interview"] = interview
    if request.method == "POST":
        form = InterviewForm(
            request.POST, instance=Interview.objects.get(InterviewID=id)
        )
        if form.is_valid():
            form.save()
            return HttpResponse(
                "<h4 id = 'main'>更新しました。画面を閉じてください</h4> <a onclick = 'window.close()'>閉じる</a>"
            )
    return render(request, "main/interview/view_interview.html", contexts)


def calc(request):
    contexts = {}
    return render(request, "main/regist/calc.html", contexts)


def export_sheet(request, id):
    contexts = {}
    if request.method == "POST":
        R_set = RegistSets.objects.get(RegistID=id)
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
        if request.POST["data"] == "two":
            name += "_include_interview"
            interviews = Interview.objects.filter(RegistID=id)
            sets["Interview"] = {
                "sheet_name": "Interviews",
                "interviews": [model_to_dict(interview) for interview in interviews],
            }
            for s in sets["Interview"]["interviews"]:
                if isinstance(s["date"], datetime):
                    s["date"] = s["date"].isoformat()
                del s["id"]
                del s["RegistID"]
                del s["InterviewID"]
        for s in sets.values():
            if "_state" in s:
                del s["_state"]
            if "company_name" in s:
                del s["company_name"]
        name += "_exported_sheet"
        if request.POST["type"] == "csv":
            response = HttpResponse(content_type="text/csv; charset=Shift-JIS")
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
    return render(request, "main/mypage/export_sheet.html", contexts)


def json_import(request):
    contexts = {}
    if request.method == "POST":
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
        return HttpResponse("<script>window.opener.location.reload();</script>")
    return render(request, "main/regist/sets/json_import.html", contexts)


@login_required
def view_main(request, control, option):
    contexts = collect_regnum(request)
    contexts["control"] = control
    menu = [
        {"choice": "top", "desc": "トップページ", "th_all": []},
        {
            "choice": "all",
            "desc": "全企業シート一覧",
            "th_all": {
                "company": "企業名",
                "company.industry": "所属業界",
                "adoption.occupation": "採用職種",
                "d_company.url": "URL",
                "created": "登録日",
                "": "詳細",
            },
        },
        {
            "choice": "interview",
            "desc": "面談録一覧",
            "th_all": ["企業名", "面談名", "面談日", "志望度(%)", "詳細"],
        },
        {
            "choice": "cat_interview",
            "desc": "カテゴリ別面談録",
            "th_all": ["企業名", "面談名", "面談日", "担当者", "志望度(%)",  "詳細"],
        },
        {
            "choice": "R_aspire",
            "desc": "志望度ランキング",
            "th_all": ["企業名", "面談回数", "志望度合計", "平均志望度", "詳細"],
        },
        {"choice": "create_custom_sheet", "desc": "カスタムシート作成", "th_all": []},
    ]
    if CustomSheet.objects.filter(by_U_ID=request.user.U_ID).count() > 0:
        for cs in CustomSheet.objects.filter(by_U_ID=request.user.U_ID):
            menu.append({"choice": cs.sheet_name, "desc": cs.sheet_name, "th_all": []})
    for m in menu:
        if m["choice"] == control:
            current_menu = m
            m["current"] = "true"
            m["active"] = "active"
        else:
            m["current"] = "false"
            m["active"] = ""

    if control == "all":
        results = RegistSets.objects.filter(
            by_U_ID=request.user.U_ID, isActive=True
        )
        if results.count() == 0:
            contexts["message"] = {
                    "type": "warning",
                    "message": "条件に一致するデータが1つもありませんでした。",
                }
        contexts["results"] = results
        contexts["th_all"] = current_menu["th_all"]

    elif control == "interview":
        options = [
            {
                "color": "outline-primary",
                "n_option": "date",
                "desc": "面談日時",
                "reverse": "",
            },
            {
                "color": "outline-primary",
                "n_option": "aspire",
                "desc": "志望度",
                "reverse": "",
            },
        ]
        contexts["options"] = options
        results = Interview.objects.filter(
            RegistID__by_U_ID=request.user.U_ID, RegistID__isActive=True
        )
        if results.count() == 0:
            contexts["message"] = {
                    "type": "warning",
                    "message": "条件に一致するデータが1つもありませんでした。",
                }
        contexts["results"] = results
        for o in options:
            if o["n_option"] == option:
                o["reverse"] = "_r"
                o["active"] = "active"
                contexts["results"] = sorted(
                    contexts["results"], key=lambda x, o=o: getattr(x, o["n_option"])
                )
            elif o["n_option"] + "_r" == option:
                o["reverse"] = ""
                o["active"] = "active"
                contexts["results"] = sorted(
                    contexts["results"],
                    key=lambda x, o=o: getattr(x, o["n_option"]),
                    reverse=True,
                )
                o["color"] = "warning"
            else:
                o["active"] = ""
        contexts["th_all"] = current_menu["th_all"]

    elif control == "R_aspire":
        R_sets = RegistSets.objects.filter(by_U_ID=request.user.U_ID, isActive=True)
        if R_sets.count() == 0:
            contexts["message"] = {
                    "type": "warning",
                    "message": "条件に一致するデータが1つもありませんでした。",
                }
        contexts["results"] = []
        for R in R_sets:
            contexts["results"].append(
                {
                    "R_sets": R,
                    "c_interview": Interview.objects.filter(RegistID=R).count(),
                    "sum_aspire": (
                        Interview.objects.filter(RegistID=R).aggregate(Sum("aspire"))[
                            "aspire__sum"
                        ]
                        if Interview.objects.filter(RegistID=R).aggregate(
                            Sum("aspire")
                        )["aspire__sum"]
                        is not None
                        else 0
                    ),
                    "avg_aspire": (
                        Interview.objects.filter(RegistID=R).aggregate(Avg("aspire"))[
                            "aspire__avg"
                        ]
                        if Interview.objects.filter(RegistID=R).aggregate(
                            Avg("aspire")
                        )["aspire__avg"]
                        is not None
                        else 0
                    ),
                }
            )
        options = [
            {
                "color": "outline-primary",
                "n_option": "c_interview",
                "desc": "面談回数",
                "reverse": "",
            },
            {
                "color": "outline-primary",
                "n_option": "sum_aspire",
                "desc": "合計志望度順",
                "reverse": "",
            },
            {
                "color": "outline-primary",
                "n_option": "avg_aspire",
                "desc": "平均志望度順",
                "reverse": "",
            },
        ]
        for o in options:
            if o["n_option"] == option:
                o["reverse"] = "_r"
                o["active"] = "active"
                contexts["results"] = sorted(
                    contexts["results"], key=lambda x, o=o: x[o["n_option"]]
                )
            elif o["n_option"] + "_r" == option:
                o["reverse"] = ""
                o["active"] = "active"
                contexts["results"] = sorted(
                    contexts["results"],
                    key=lambda x, o=o: x[o["n_option"]],
                    reverse=True,
                )
                o["color"] = "warning"
            else:
                o["active"] = ""
        contexts["options"] = options
        contexts["th_all"] = current_menu["th_all"]

    elif control == "cat_interview":
        results = Interview.objects.filter(
            RegistID__by_U_ID=request.user.U_ID, RegistID__isActive=True
        )
        if results.count() == 0:
            contexts["message"] = {
                    "type": "warning",
                    "message": "条件に一致するデータが1つもありませんでした。",
                }
        if option != "default":
            if results.filter(tag=option).count() == 0:
                contexts["message"] = {
                    "type": "warning",
                    "message": "条件に一致する面談録がありませんでした。",
                }
            else:
                results = results.filter(tag=option)
        contexts["results"] = results
        choices = Interview.tags
        contexts["choices"] = choices
        contexts["th_all"] = current_menu["th_all"]

    elif control == "top":
        contexts["message"] = {
            "type": "success",
            "message": "左のメニューから選択してください。(カスタムシートで指定した場合を除き、活動中の企業のみ表示されます)",
        }
    elif control == "create_custom_sheet":
        return redirect("create_custom_sheet")
    else:
        if control in [
            cs.sheet_name
            for cs in CustomSheet.objects.filter(by_U_ID=request.user.U_ID)
        ]:
            contexts["customsheet"] = "true"
            cs = CustomSheet.objects.get(sheet_name=control)
            results = apps.get_model("main", cs.model).objects.all()
            if cs.search_settings != {}:
                if cs.search_settings["how"] == "1":
                    results = results.filter(
                        **{cs.search_settings["where"]: cs.search_settings["what"]}
                    )
                elif cs.search_settings["how"] == "2":
                    results = results.filter(
                        **{
                            f"{cs.search_settings['where']}__contains": cs.search_settings[
                                "what"
                            ]
                        }
                    )
                elif cs.search_settings["how"] == "3":
                    results = results.filter(
                        **{
                            f"{cs.search_settings['where']}__gte": cs.search_settings[
                                "what"
                            ]
                        }
                    )
                elif cs.search_settings["how"] == "4":
                    results = results.filter(
                        **{
                            f"{cs.search_settings['where']}__lte": cs.search_settings[
                                "what"
                            ]
                        }
                    )
            if cs.view_settings != {}:
                if cs.view_settings[list(cs.view_settings.keys())[0]] == "1":
                    results = results.order_by(list(cs.view_settings.keys())[0])
                elif cs.view_settings[list(cs.view_settings.keys())[0]] == "2":
                    results = results.order_by(
                        list(cs.view_settings.keys())[0]
                    ).reverse()
            if results.count() == 0:
                contexts["message"] = {
                    "type": "warning",
                    "message": "条件に一致するデータが1つもありませんでした。",
                }
            contexts["sheet_config"] = {
                "model": cs.model,
                "selected": cs.selected_field,
                "view_settings": cs.view_settings,
                "search_settings": cs.search_settings,
                "sheet_id": cs.sheet_id,
            }
            contexts["results"] = results
            contexts["th_all"] = cs.selected_field
        else:
            contexts["message"] = {
                "type": "danger",
                "message": "不正なリクエストです。",
            }

    contexts["menu"] = menu
    return render(request, "main/view/main.html", contexts)


def create_custom_sheet(request):
    contexts = collect_regnum(request)
    contexts["model_names"] = {
        model.__name__: model._meta.verbose_name
        for model in apps.get_models()
        if model.__name__
        not in [
            "LogEntry",
            "Permission",
            "Group",
            "User",
            "CustomUser",
            "Session",
            "Site",
            "ContentType",
            "AdminLog",
            "CustomSheet",
        ]
    }
    if "model" in request.GET:
        if request.GET["model"] == "default":
            return redirect("create_custom_sheet")
        if request.GET["create_sheet_name"] == "":
            contexts["message"] = {
                "type": "danger",
                "message": "シート名を入力してください",
            }
            return render(request, "main/view/customsheet/create.html", contexts)
        else:
            if (
                CustomSheet.objects.filter(
                    sheet_name=request.GET["create_sheet_name"]
                ).count()
                > 0
            ):
                contexts["message"] = {
                    "type": "danger",
                    "message": "そのシート名は既に使用されています。",
                }
                return render(request, "main/view/customsheet/create.html", contexts)
            contexts["model_selected"] = request.GET["model"]
            if request.GET["model"] not in contexts["model_names"]:
                contexts["message"] = {
                    "type": "danger",
                    "message": "不正なリクエストです。",
                }
                return render(request, "main/view/customsheet/create.html", contexts)
            model = apps.get_model("main", request.GET["model"])
            contexts["model_fields"] = {
                field.name: field.verbose_name if hasattr(field, 'verbose_name') else field.name
                for field in model._meta.get_fields()
                if field.name
                not in [
                    "id",
                    "RegistID",
                    "InterviewID",
                    "regist_publish",
                    "AdoptionID",
                    "D_CompanyID",
                    "MotivationID",
                    "IdeaID",
                    "AboutID",
                    "CompanyID",
                    "by_U_ID",
                ]
            }
            contexts["sheet_name_form"] = request.GET["create_sheet_name"]
            contexts["message"] = {
                "type": "success",
                "message": "選択したモデルを確認し、抽出対象のフィールドと、必要であれば表示名を指定してください",
            }

    if request.method == "POST":
        if request.POST["request_type"] == "select_model_and_field":
            res = {}
            for x, y in zip(request.POST.getlist("selected_field"), request.POST.getlist("selected_field_name")):
                res[x] = y
            contexts["selected_field"] = res
            contexts["model_fields"] = ""
            contexts["message"] = {
                "type": "success",
                "message": "指定したフィールドと表示名を確認し、表示順の指定、検索対象と検索条件を指定してください",
            }
        if request.POST["request_type"] == "view_setting":
            contexts["model_fields"] = ""
            data = {
                "create_sheet_name": request.POST.get("create_sheet_name"),
                "select_model": request.POST.get("model"),
                "selected_field": {
                    x: y
                    for x, y in zip(
                        request.POST.getlist("selected_field"),
                        request.POST.getlist("selected_field_name"),
                    )
                },
                "view_setting": request.POST.get("view_setting"),
                "view_setting_order": request.POST.get("view_setting_order"),
                "view_setting_search_how": request.POST.get("view_setting_search_how"),
                "view_setting_search": request.POST.get("view_setting_search"),
                "view_setting_search_string": request.POST.get(
                    "view_setting_search_string"
                ),
            }
            request.session["result_data"] = data
            contexts["result_data"] = data
            contexts["message"] = {
                "type": "success",
                "message": "以下の内容で登録されます。内容を確認してください",
            }
        if request.POST["request_type"] == "create_sheet":
            data = request.session["result_data"]
            CustomSheet.objects.create(
                sheet_id=secrets.token_hex(32),
                sheet_name=data["create_sheet_name"],
                model=data["select_model"],
                selected_field=data["selected_field"],
                view_settings=(
                    {data["view_setting"]: data["view_setting_order"]}
                    if data["view_setting"] != ""
                    else {}
                ),
                by_U_ID=request.user.U_ID,
                search_settings=(
                    {
                        "how": data["view_setting_search_how"],
                        "where": data["view_setting_search"],
                        "what": data["view_setting_search_string"],
                    }
                    if data["view_setting_search_how"] != ""
                    else {}
                ),
            )
            del request.session["result_data"]
            return HttpResponse(
                f"登録が完了しました。<a href ='{reverse('view_main', kwargs=dict(control='top',option='default' ))}'>戻る</a>"
            )
    return render(request, "main/view/customsheet/create.html", contexts)


def delete_custom_sheet(request, id):
    contexts = collect_regnum(request)
    cs = CustomSheet.objects.get(sheet_id=id)
    contexts["sheet_config"] = {
        "model": cs.model,
        "selected": cs.selected_field,
        "view_settings": cs.view_settings,
        "search_settings": cs.search_settings,
        "sheet_id": cs.sheet_id,
    }
    if request.method == "POST":
        CustomSheet.objects.filter(sheet_id=id).delete()
        return HttpResponse(
            f"削除しています...<script>window.opener.location.href='{reverse('view_main', kwargs=dict(control='top',option='default' ))}'</script>"
        )
    return render(request, "main/view/customsheet/delete.html", contexts)


def change_active(request):
    if request.method == "POST":
        RegistSets.objects.filter(RegistID=request.POST.get("RegistID")).update(
            isActive=(True if request.POST.get("current_status") != "True" else False)
        )
    return HttpResponse("<script>window.opener.location.reload()</script>")


def get_interviewer(request, id):
    return JsonResponse({"interviewer": RegistSets.objects.get(RegistID=id).company.contact})
