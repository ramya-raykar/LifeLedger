from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email Address",
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email address"})
    )

    class Meta(UserCreationForm.Meta):
        model=get_user_model()
        fields=("username", "email")
        labels={
            "username": "Username"
        }
        widgets={
            "username": forms.TextInput(attrs={"placeholder": "Choose a username"})
        }