from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import View
from dms.forms.login_form import LoginForm
from dms.forms.password_form import PasswordForm
from django.conf import settings
from dms.models import User, UserProfile
from dms.tasks import send_email


class Login(View):
    def post(self, request, *args, **kwargs):
        if request.POST.get('resetPass', None):
            form = PasswordForm(request.POST)
            if form.is_valid():
                user = User.objects(username=form.cleaned_data['username'], \
                                           email=form.cleaned_data['email']).first()
                profile = UserProfile.objects(user=user).first()
                if user:
                    name = profile.name if profile else 'DMS User'
                    subject = 'NECOC Password Reset Request'
                    from_email = settings.DEFAULT_FROM_EMAIL
                    user_id = user.id
                    hostname = settings.HOSTNAME
                    admin_email = settings.ADMIN_EMAIL
                    message = settings.PASSWORD_RESET_REQUEST_MESSAGE % \
                              {'name': name,
                               'hostname': hostname,
                               'user_id': user_id,
                               'admin_email': admin_email}
                    recipient_list = [user.email]
                    send_email.delay(subject, message, from_email, recipient_list)
                else:
                    form.add_error(None, 'No user with matching Username and Password')
            else:
                form.add_error(None, 'Invalid data')
        else:
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