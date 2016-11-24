from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import View
from dms.forms.login_form import LoginForm
from dms.forms.password_form import PasswordForm
from django.conf import settings
from dms.models import User, UserProfile
from mongoengine.django.auth import UserManager
from dms.tasks import send_email, send_one_sms


class Login(View):
    def post(self, request, *args, **kwargs):
        if request.POST.get('resetPass', None):
            form = PasswordForm(request.POST)
            if form.is_valid():
                user = User.objects(username=form.cleaned_data['username'],
                                    email=form.cleaned_data['email']).first()
                profile = UserProfile.objects(user=user).first()
                if user:
                    name = profile.name if profile else 'DMS User'
                    phone = profile.phone if profile else ''
                    subject = 'NECOC Password Reset Request'
                    from_email = settings.DEFAULT_FROM_EMAIL
                    hostname = settings.HOSTNAME
                    admin_email = settings.ADMIN_EMAIL
                    password = UserManager().make_random_password()
                    user.set_password(password)
                    user.save()

                    message = settings.RESET_PASSWORD_MESSAGE % {
                        'name': name,
                        'hostname': hostname,
                        'password': password,
                        'admin_email': admin_email}
                    recipient_list = [user.email]
                    send_email.delay(subject, message, from_email, recipient_list)
                    if phone and getattr(settings, 'SENDSMS_ON_PASSWORD_RESET', False):
                        text = 'Your NECOC password for user: %s has been reset to %s' % (user.username, password)
                        send_one_sms.delay(None, phone, text)
                else:
                    form.add_error(None, 'No user with matching Username and Email')
            else:
                form.add_error(None, 'Invalid data')
            return render(request, 'login.html', {'form': form})
        else:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = authenticate(username=(login_form.cleaned_data['username']),
                                    password=(login_form.cleaned_data['password']))
                if user:
                    login(request, user)
                    return redirect('/')
                login_form.add_error(None, 'Username or Password is invalid')
            return render(request, 'login.html', {'login_form': login_form})

    def get(self, request, *args, **kwargs):
        login_form = LoginForm()
        form = PasswordForm()
        return render(request, 'login.html', {'login_form': login_form, 'form': form})


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/login/')