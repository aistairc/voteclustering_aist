from django.shortcuts import redirect


def logout(request):
    request.session.flush()
    return redirect("login")
