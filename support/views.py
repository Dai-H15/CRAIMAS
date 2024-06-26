import secrets
from django.http import HttpResponse
from django.shortcuts import render

from main.views import collect_regnum
from .forms import SupportForm
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def support_post(request):
    contexts = collect_regnum(request)
    form = SupportForm()
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            s = form.save(commit=False)
            TicketID = secrets.token_hex(32)
            s.TicketID = TicketID
            s.request_by = request.user
            s.save()
            contexts["TicketID"] = TicketID
            return render(request, "support/done.html", contexts)
        else:
            return HttpResponse("不正なリクエストです。管理者に問い合わせてください。")
    contexts["form"] = form
    return render(request, "support/main.html", contexts)