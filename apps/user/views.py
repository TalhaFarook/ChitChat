from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.chat.models import OneChat, UserTable

from .forms import ChangePasswordForm, ForgetPasswordForm, LoginForm, SignUpForm


class LogoutView(View):
    def get(self, request):
        user = request.user
        user.current_active = 0
        user.save()
        logout(request)
        return redirect("user:login")


class SignupView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, "signup_form.html", {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("user:login")


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        messages = OneChat.objects.filter(receiver_id=request.user.id)
        if messages:
            for message in messages:
                message.is_delivered = True
                message.save()
        return render(request, "dashboard.html", {"username": request.user.username})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login_form.html", {"form": form, "login_failed": False})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                user.current_active = 1
                user.save()
                login(request, user)
                messages = OneChat.objects.filter(receiver_id=request.user.id)
                if messages:
                    for message in messages:
                        message.is_delivered = True
                        message.save()
                return redirect("user:dashboard")
            else:
                return render(
                    request, "login_form.html", {"form": form, "login_failed": True}
                )


class ForgetPasswordView(View):
    def get(self, request):
        form = ForgetPasswordForm()
        return render(
            request, "forget_password_form.html", {"form": form, "forget_failed": 0}
        )

    def post(self, request):
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["email"]:
                user_obj = UserTable.objects.filter(email=form.cleaned_data["email"])
                if user_obj:
                    return render(
                        request,
                        "forget_password_form.html",
                        {"form": form, "forget_failed": 2},
                    )
                else:
                    return render(
                        request,
                        "forget_password_form.html",
                        {"form": form, "forget_failed": 1},
                    )


class ChangePasswordView(View):
    def get(self, request):
        form = ChangePasswordForm()
        return render(
            request, "change_password_form.html", {"form": form, "change_failed": False}
        )

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data["old_password"]
            user = authenticate(request, username=request.user, password=old_password)
            if user:
                user.set_password(form.cleaned_data["new_password"])
                user.save()
                return redirect("user:login")
