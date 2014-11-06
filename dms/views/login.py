from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import View
from dms.forms.login_form import LoginForm


class Login(View):
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=(form.cleaned_data['username']), password=(form.cleaned_data['password']))
            if user:
                login(request, user)
                return redirect('/')
            form.add_error(None, 'Username or Password is invalid')
        return render(request, 'login.html', {'form': form})

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/login/')