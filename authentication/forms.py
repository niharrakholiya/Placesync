# forms.py

from django import forms
from .models import Student, Company, BasicUser, JobPost


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = BasicUser
        exclude = ['role','is_active', 'is_staff','last_login']
        widgets = {
            'password': forms.PasswordInput(),
        }
class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user']


class StudentLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class CompanyRegistrationForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['user']
        fields = ['company_name', 'company_location', 'company_image', 'company_link' , 'about']  # Include 'company_name' field


class CompanyLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['total_posts', 'positions', 'salary', 'location']