from django.shortcuts import render, redirect
from .models import Companies, About, RegistSets
from authUser.models import CustomUser
from .forms import CompaniesForm, AboutForm, IdeaForm, MotivationForm, D_CompanyForm, AdoptionForm

# Functions


def collect_regnum():
    res = {
        "num_c": Companies.objects.count(),
        "num_a": About.objects.count(),
        }
    return res


def collect_regsets(user):
    res = RegistSets.objects.filter(by_c_id=user.c_id)
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
    if request.user.is_authenticated:
        contexts = collect_regnum()
        user = CustomUser.objects.get(username=request.user)
        contexts["user"] = user
        n_regist = RegistSets.objects.filter(by_c_id=user.c_id).count()
        contexts["n_regist"] = n_regist
        contexts["regsets"] = collect_regsets(user)
    else:
        redirect(to="auth/login")
    return render(request, "main/mypage.html", contexts)
