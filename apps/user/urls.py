from django.urls import path

from . import views

# Define the app namespace
app_name = "user"

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("", views.LoginView.as_view(), name="login"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "forget-password/", views.ForgetPasswordView.as_view(), name="forget-password"
    ),
    path(
        "change-password/", views.ChangePasswordView.as_view(), name="change-password"
    ),
]
