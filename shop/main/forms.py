from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={ 'placeholder': 'Username', 'class': 'form-control' }))
    email = forms.CharField(widget=forms.EmailInput(attrs={ 'placeholder': 'Email', 'class': 'form-control' }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={ 'placeholder': 'Password', 'class': 'form-control' }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={ 'placeholder': 'Confirm Password', 'class': 'form-control' }))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'
    
    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={ 'placeholder': 'Username', 'class': 'form-control' }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={ 'placeholder': 'Password', 'class': 'form-control' }))
    
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
