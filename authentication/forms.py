# forms.py

from django import forms
from .models import Student
from .models import Company


class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class StudentLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class CompanyRegistrationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['username', 'email', 'password', 'company_name', 'company_location']  # Include 'company_name' field
        widgets = {
            'password': forms.PasswordInput(),
        }


class CompanyLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
