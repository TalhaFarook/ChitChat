from django import forms

from .models import UserTable


# Form for user registration (sign-up)
class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserTable
        fields = ["username", "email", "password"]


# Form for user login
class LoginForm(forms.Form):
    username = forms.CharField(max_length=12)
    password = forms.CharField(widget=forms.PasswordInput)


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField()


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Old password")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New password")
