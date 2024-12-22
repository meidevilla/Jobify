from django import forms
from .models import JobApplication, Reminders, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import UserChangeForm

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['company_name', 'position', 'location',  'work_setup', 'status', 'date_applied', 'interview_schedule', 'job_posting_url']
        widgets = {
            'position': forms.TextInput(attrs={'required': 'required'}),
            'company_name': forms.TextInput(attrs={'required': 'required'}),
            'date_applied': forms.DateInput(attrs={'required': 'required', 'type': 'date'}),
            'status': forms.Select(attrs={'required': 'required'}),
        }

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'first name', 'class': 'form-control', }))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'last name', 'class': 'form-control', }))
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'username', 'class': 'form-control', }))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'e-mail address', 'class': 'form-control',}))
    password1 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'form-control','data-toggle': 'password', 'id': 'password',}))
    password2 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'confirm password', 'class': 'form-control', 'data-toggle': 'password','id': 'password',}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[0-9]', password):
            raise ValidationError('Password must contain at least one digit.')
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError('Passwords do not match. Please try again.')
        return password2

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'username', 'class': 'form-control', }))
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'form-control','data-toggle': 'password', 'id': 'password',}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError("Please enter your username.")
        return username
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("Please enter your password.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            if username != "expected_username" or password != "expected_password":
                raise forms.ValidationError("Invalid username or password.")
        return cleaned_data
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']

class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['username'].required = False
        self.fields['email'].required = False
        self.fields['email'].widget.attrs['disabled'] = 'disabled'

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

class RemindersForm(forms.ModelForm):
    class Meta:
        model = Reminders
        fields = ['title', 'description', 'reminder_time']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Write the reminder description.', 'class': 'form-control'}),
            'reminder_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

