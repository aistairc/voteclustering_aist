from django.shortcuts import render, redirect
from AIST_survey.models import Enquete


def login(request):
    if "enquete_id" in request.session:
        return redirect("index")
    return render(request, 'dashboard/login.html')


def login_auth(request):
    if "access_token" not in request.POST:
        return redirect("login")
    access_token = request.POST['access_token']
    if len(access_token) == 0:
        return render(request, 'dashboard/login.html', {"error": "no_input"})
    enquete = Enquete.compare_access_token(access_token)
    if enquete is None:
        return render(request, 'dashboard/login.html', {"error": "invalid_access_token"})
    request.session["enquete_id"] = enquete.id
    return redirect("index")
