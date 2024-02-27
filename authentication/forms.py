# forms.py

from django import forms
from .models import Student


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
