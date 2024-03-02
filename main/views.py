from django.shortcuts import render, redirect,HttpResponse
from .models import Companies, About, RegistSets, Idea, Motivation, D_Company, Adoption
from authUser.models import CustomUser
from .forms import CompaniesForm, AboutForm, IdeaForm, MotivationForm, D_CompanyForm, AdoptionForm
import secrets

# Functions


def collect_regnum():
    res = {
        "num_c": Companies.objects.count(),
        "num_a": About.objects.count(),
        }
    return res


def collect_regsets(user):
    res = RegistSets.objects.filter(by_U_ID=user.U_ID)
    return res

# Views
def index(request):
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
        post = RegistSets.objects.get(RegistID=id)
        C_Form = CompaniesForm(instance=post.company)
        A_Form = AboutForm(instance=post.about)
        I_Form = IdeaForm(instance=post.idea)
        M_Form = MotivationForm(instance=post.motivation)
        D_Form = D_CompanyForm(instance=post.d_company)
        AD_Form = AdoptionForm(instance=post.adoption)
        print(C_Form)
        contexts["post"] = post
        contexts["C_Form"] = C_Form
        contexts["A_Form"] = A_Form
        contexts["I_Form"] = I_Form
        contexts["M_Form"] = M_Form
        contexts["D_Form"] = D_Form
        contexts["AD_Form"] = AD_Form
    except RegistSets.DoesNotExist:
        return redirect(to="mypage")
    return render(request, "main/view_my_post.html", contexts)
