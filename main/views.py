from django.shortcuts import render, redirect, HttpResponse
from .models import Companies, About, RegistSets, Idea, Motivation, D_Company, Adoption
from authUser.models import CustomUser
from .forms import CompaniesForm, AboutForm, IdeaForm, MotivationForm, D_CompanyForm, AdoptionForm
import secrets

# Functions


def collect_regnum():
    res = {
        "num_c": Companies.objects.count(),
        "num_a": RegistSets.objects.count(),
        }
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
    if "CampanyID" in request.session:
        del request.session["CampanyID"]
    contexts = collect_regnum()
    return render(request, "main/index.html", contexts)


def regist_base(request):
    contexts = collect_regnum()
    return render(request, "main/regist_base.html", contexts)


def regist_all(request):
    contexts = collect_regnum()
    if request.method == "POST":
        C_Form = CompaniesForm(request.POST)
        A_Form = AboutForm(request.POST)
        I_Form = IdeaForm(request.POST)
        M_Form = MotivationForm(request.POST)
        D_Form = D_CompanyForm(request.POST)
        AD_Form = AdoptionForm(request.POST)
        if C_Form.is_valid() and A_Form.is_valid() and I_Form.is_valid() and M_Form.is_valid() and D_Form.is_valid() and AD_Form.is_valid():
            CompanyID = secrets.token_hex(64)
            n_CForm = C_Form.save(commit=False)
            n_CForm.CompanyID = CompanyID
            n_CForm.save()

            C_Data = Companies.objects.get(CompanyID=CompanyID)
            n_AForm = A_Form.save(commit=False)
            n_AForm.company_name = C_Data
            n_IForm = I_Form.save(commit=False)
            n_IForm.company_name = C_Data
            n_MForm = M_Form.save(commit=False)
            n_MForm.company_name = C_Data
            n_DForm = D_Form.save(commit=False)
            n_DForm.company_name = C_Data
            n_ADForm = AD_Form.save(commit=False)
            n_ADForm.company_name = C_Data

            n_AForm.save()
            n_IForm.save()
            n_MForm.save()
            n_DForm.save()
            n_ADForm.save()

            n_RegistSets = RegistSets.objects.create(
                RegistID=secrets.token_hex(64),
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
            return render(request, "main/regist_done.html", contexts)
    C_Form = CompaniesForm()
    contexts["C_Form"] = C_Form

    A_Form = AboutForm()
    contexts["A_Form"] = A_Form

    I_Form = IdeaForm()
    contexts["I_Form"] = I_Form

    M_Form = MotivationForm()
    contexts["M_Form"] = M_Form

    D_Form = D_CompanyForm()
    contexts["D_Form"] = D_Form

    AD_Form = AdoptionForm()
    contexts["AD_Form"] = AD_Form
    
    return render(request, "main/regist_all.html", contexts)


def show_data(request):
    companies = Companies.objects.all()
    contexts = {
        "companies": companies,
    }
    return render(request, "main/show.html", contexts)


def mypage(request):
    contexts = collect_regnum()
    if request.user.is_authenticated:
        user = CustomUser.objects.get(username=request.user)
        contexts["user"] = user
        n_regist = RegistSets.objects.filter(by_U_ID=user.U_ID).count()
        contexts["n_regist"] = n_regist
        contexts["regsets"] = collect_regsets(user)
        posts = RegistSets.objects.filter(by_U_ID=request.user.U_ID)
        contexts["posts"] = posts
    else:
        return redirect(to="login")
    return render(request, "main/mypage.html", contexts)


def view_my_post(request, id):
    contexts = {}
    try:
        contexts = getRegistSets(id, contexts)
    except RegistSets.DoesNotExist:
        return redirect(to="mypage")
    return render(request, "main/view_my_post.html", contexts)


def delete_posts(request, id):
    contexts = getRegistSets(id, {})
    if request.method == "POST":
        if "del_C_Form" in request.POST:
            try:
                post = Companies.objects.get(CompanyID=RegistSets.objects.get(RegistID=id).company.CompanyID)
                post.delete()
                RegistSets.objects.get(RegistID=id).delete()
            except:
                RegistSets.objects.get(RegistID=id).delete()
        else:
            post = RegistSets.objects.get(RegistID=id)
            print(request.POST)
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
        return redirect(to="mypage")
    return render(request, "main/delete.html", contexts)


def regist_sets(request):
    contexts = collect_regnum()
    return render(request, "main/sets/main.html", contexts)


def create_company(request):
    contexts = collect_regnum()
    if request.method == "POST":
        C_Form = CompaniesForm(request.POST)
        if C_Form.is_valid():
            CompanyID = secrets.token_hex(64)
            n_CForm = C_Form.save(commit=False)
            n_CForm.CompanyID = CompanyID
            n_CForm.save()
            Temp_regist = RegistSets.objects.create(RegistID=secrets.token_hex(64), by_U_ID=CustomUser.objects.get(username=request.user), company=Companies.objects.get(CompanyID=CompanyID))
            request.session["RegistID"] = Temp_regist.RegistID
            print("new company created.")
            return redirect("create_about")
    C_Form = CompaniesForm()
    contexts["C_Form"] = C_Form
    return render(request, "main/sets/create_company.html", contexts)


def import_company(request):
    contexts = collect_regnum()
    if request.method == "POST":
        if "import" in request.POST:
            copy_company = Companies.objects.get(CompanyID=request.POST["ID"])
            CompanyID = secrets.token_hex(64)
            copy_company.CompanyID = CompanyID
            copy_company.save()
            Temp_regist = RegistSets.objects.create(RegistID=secrets.token_hex(64), by_U_ID=CustomUser.objects.get(username=request.user), company=Companies.objects.get(CompanyID=CompanyID))
            request.session["RegistID"] = Temp_regist.RegistID
            return redirect("create_about")
    companies = Companies.objects.all()
    contexts["posts"] = companies
    return render(request, "main/sets/import_company.html", contexts)


def create_about(request):
    contexts = collect_regnum()
    A_Form = AboutForm()
    contexts["A_Form"] = A_Form
    contexts["C_Form"] = CompaniesForm(instance=RegistSets.objects.get(RegistID=request.session["RegistID"]).company)
    if request.method == "POST":
        A_Form = AboutForm(request.POST)
        if A_Form.is_valid():
            n_AForm = A_Form.save(commit=False)
            n_AForm.company_name = RegistSets.objects.get(RegistID=request.session["RegistID"]).company
            AboutID = secrets.token_hex(64)
            n_AForm.AboutID = AboutID
            n_AForm.save()
            Temp_regist = RegistSets.objects.get(RegistID=request.session["RegistID"])
            Temp_regist.about = About.objects.get(AboutID=AboutID)
            Temp_regist.save()
            return redirect("create_idea")

    return render(request, "main/sets/create_about.html", contexts)


def create_idea(request):
    contexts = collect_regnum()
    contexts["A_Form"] = AboutForm(instance=RegistSets.objects.get(RegistID=request.session["RegistID"]).about)
    I_Form = IdeaForm()
    contexts["I_Form"] = I_Form
    if request.method == "POST":
        I_Form = IdeaForm(request.POST)
        if I_Form.is_valid():
            n_IForm = I_Form.save(commit=False)
            n_IForm.company_name = RegistSets.objects.get(RegistID=request.session["RegistID"]).company
            IdeaID = secrets.token_hex(64)
            n_IForm.IdeaID = IdeaID
            n_IForm.save()
            Temp_regist = RegistSets.objects.get(RegistID=request.session["RegistID"])
            Temp_regist.idea = Idea.objects.get(IdeaID=IdeaID)
            Temp_regist.save()
            return redirect("create_motivation")
    return render(request, "main/sets/create_idea.html", contexts)


def create_motivation(request):
    contexts = collect_regnum()
    contexts["I_Form"] = IdeaForm(instance=RegistSets.objects.get(RegistID=request.session["RegistID"]).idea)
    M_Form = MotivationForm()
    contexts["M_Form"] = M_Form
    if request.method == "POST":
        M_Form = MotivationForm(request.POST)
        if M_Form.is_valid():
            n_MForm = M_Form.save(commit=False)
            n_MForm.company_name = RegistSets.objects.get(RegistID=request.session["RegistID"]).company
            MotivationID = secrets.token_hex(64)
            n_MForm.MotivationID = MotivationID
            n_MForm.save()
            Temp_regist = RegistSets.objects.get(RegistID=request.session["RegistID"])
            Temp_regist.motivation = Motivation.objects.get(MotivationID=MotivationID)
            Temp_regist.save()
            return redirect("create_d_company")
    return render(request, "main/sets/create_motivation.html", contexts)


def create_d_company(request):
    contexts = collect_regnum()
    contexts["M_Form"] = MotivationForm(instance=RegistSets.objects.get(RegistID=request.session["RegistID"]).motivation)
    D_Form = D_CompanyForm()
    contexts["D_Form"] = D_Form
    if request.method == "POST":
        D_Form = D_CompanyForm(request.POST)
        if D_Form.is_valid():
            n_DForm = D_Form.save(commit=False)
            n_DForm.company_name = RegistSets.objects.get(RegistID=request.session["RegistID"]).company
            D_CompanyID = secrets.token_hex(64)
            n_DForm.D_CompanyID = D_CompanyID
            n_DForm.save()
            Temp_regist = RegistSets.objects.get(RegistID=request.session["RegistID"])
            Temp_regist.d_company = D_Company.objects.get(D_CompanyID=D_CompanyID)
            Temp_regist.save()
            return redirect("create_adoption")
    return render(request, "main/sets/create_d_company.html", contexts)


def create_adoption(request):
    contexts = collect_regnum()
    contexts["D_Form"] = D_CompanyForm(instance=RegistSets.objects.get(RegistID=request.session["RegistID"]).d_company)
    AD_Form = AdoptionForm()
    contexts["AD_Form"] = AD_Form
    if request.method == "POST":
        AD_Form = AdoptionForm(request.POST)
        if AD_Form.is_valid():
            n_ADForm = AD_Form.save(commit=False)
            n_ADForm.company_name = RegistSets.objects.get(RegistID=request.session["RegistID"]).company
            AdoptionID = secrets.token_hex(64)
            n_ADForm.AdoptionID = AdoptionID
            n_ADForm.save()
            Temp_regist = RegistSets.objects.get(RegistID=request.session["RegistID"])
            Temp_regist.adoption = Adoption.objects.get(AdoptionID=AdoptionID)
            Temp_regist.save()
            return redirect("create_complete")
    return render(request, "main/sets/create_adoption.html", contexts)


def create_complete(request):
    contexts = collect_regnum()
    regist = RegistSets.objects.get(RegistID=request.session["RegistID"])
    del request.session["RegistID"]
    contexts["C_Form"] = CompaniesForm(instance=regist.company)
    contexts["A_Form"] = AboutForm(instance=regist.about)
    contexts["I_Form"] = IdeaForm(instance=regist.idea)
    contexts["M_Form"] = MotivationForm(instance=regist.motivation)
    contexts["D_Form"] = D_CompanyForm(instance=regist.d_company)
    contexts["AD_Form"] = AdoptionForm(instance=regist.adoption)
    return render(request, "main/sets/create_complete.html", contexts)


def edit_posts(request, id):
    contexts = getRegistSets(id, collect_regnum())
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
        if A_Form.is_valid() and I_Form.is_valid() and M_Form.is_valid() and D_Form.is_valid() and AD_Form.is_valid():
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
            return redirect("mypage")

    return render(request, "main/edit_posts.html", contexts)
