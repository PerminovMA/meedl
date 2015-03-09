__author__ = 'PerminovMA@live.ru'

from django.shortcuts import render, redirect
from control_panel_app.forms.authorization_forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout


def login_page(request):
    if request.user.is_authenticated():
        return redirect('control_panel:index_url')

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            if not username or not password:
                return HttpResponse("Bad request")

            user = authenticate(username = username, password = password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('control_panel:index_url')
                else:
                    context = {'disabled_account': True}
            else:
                print form.cleaned_data
                context = {'access_denied': True}
    else:
        context = {}

    form = LoginForm()
    context["login_form"] = form
    return render(request, 'control_panel_app/login_page.html', context)


def logout_view(request):
    logout(request)
    return redirect('control_panel:login_url')