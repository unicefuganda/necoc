from django import forms


class PasswordForm(forms.Form):
    username = forms.CharField(label='Username')
    email = forms.CharField(label='Email Address', widget=forms.EmailInput)