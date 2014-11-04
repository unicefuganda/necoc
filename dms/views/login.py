from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.views.generic import View
from dms.forms.login_form import LoginForm


class Login(View):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=(form.cleaned_data['username']), password=(form.cleaned_data['password']))
            if user:
                login(request, user)
                return render(request, 'index.html')
            else:
                form.add_error(None, 'Username or Password is invalid')
                return render(request, 'login.html', {'form': form})
        return render(request, 'login.html', {'form': form})

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


