from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import secrets

# Create your views here.


def signup_view(request):
    if request.method == 'POST':

        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.c_id = secrets.token_hex(32)
            user.y_graduation = 2099
            user.save()
            login(request, user)
            return redirect(to='/')

    else:
        form = SignupForm()

    param = {
        'form': form
    }

    return render(request, 'registration/signup.html', param)
