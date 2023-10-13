from django import forms
from .models import UserTable

# Form for user registration (sign-up)
class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = UserTable
        # Specify the fields to be included in the form
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        # Create a new user instance based on the form data
        user = super().save(commit=False)

        if commit:
            # Save the user to the database
            user.save()

        return user

# Form for user login
class LoginForm(forms.Form):
    # Specify required fields for log in
    username = forms.CharField(max_length=12)
    password = forms.CharField(widget=forms.PasswordInput)
