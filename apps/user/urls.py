from django.urls import path
from . import views

# Define the app namespace
app_name = 'user'

urlpatterns = [
    # URL pattern for user registration (Sign Up)
    path('signup/', views.signup_view, name='signup'),

    # URL pattern for user login
    path('login/', views.login_view, name='login'),

    # This empty path can serve as the login page
    path('', views.login_view, name='login'),

    # URL pattern for the user's dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # URL pattern for user logout
    path('logout/', views.logout_view, name='logout'),

    # URL pattern for forget password
    path('forget-password/', views.forget_password_view, name='forget-password'),

    # URL pattern for change password
    path('change-password/', views.change_password_view, name='change-password'),
]
