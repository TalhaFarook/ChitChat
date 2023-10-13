from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from apps.chat.models import OneChat
from django.contrib.auth.decorators import login_required

# View for user logout
@login_required
def logout_view(request):
    # Get the current user
    user = request.user

    # Set the user's current_active status to 0
    user.current_active = 0
    user.save()

    # Log out the user and redirect to the login page
    logout(request)
    return redirect('user:login')

# View for user registration (Sign Up)
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():

            # Create a new user based on the form data
            user = form.save(commit=False)
            user.is_active = True
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Redirect to the login page after successful registration
            return redirect('user:login')
    else:
        form = SignUpForm()

    return render(request, 'signup_form.html', {'form': form})

# View for the user's dashboard, requires login
@login_required
def dashboard_view(request):
    # Mark delivered messages as 'is_delivered' when user logs into their account 
    messages = OneChat.objects.filter(receiver_id=request.user.id)
    if messages:
        for message in messages:
            message.is_delivered = True
            message.save()

    return render(request, 'dashboard.html', {'username': request.user.username})

# View for user login
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                user.current_active = 1
                user.save()

                # Log in the user and redirect to the dashboard
                login(request, user)

                # Mark delivered messages as 'is_delivered' when user logs into their account 
                messages = OneChat.objects.filter(receiver_id=request.user.id)
                if messages:
                    for message in messages:
                        message.is_delivered = True
                        message.save()

                return redirect('user:dashboard')
            else:
                return render(request, 'login_form.html', {'form': form, 'login_failed': True})
    else:
        form = LoginForm()

    return render(request, 'login_form.html', {'form': form, 'login_failed': False})
