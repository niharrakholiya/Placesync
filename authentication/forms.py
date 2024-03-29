# forms.py

from django import forms
from .models import Student, Company, BasicUser, JobPost


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = BasicUser
        exclude = ['role', 'is_active', 'is_staff', 'last_login']
        widgets = {
            'password': forms.PasswordInput(),

        }


class StudentLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class CompanyRegistrationForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['user']
        fields = ['company_name', 'company_location', 'company_image', 'company_link', 'about']  # Include 'company_name' field


class CompanyLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['total_posts', 'positions', 'salary', 'location']

class StudentRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    gender = forms.ChoiceField(choices=(('Male', 'Male'), ('Female', 'Female')), required=True)
    age = forms.IntegerField(required=True)
    dob = forms.DateField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), min_length=8, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), min_length=8, required=True)
    phone_number = forms.CharField(max_length=10, required=True)
    address = forms.CharField(widget=forms.Textarea, max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)
    pincode = forms.CharField(max_length=6, required=True)
    hobbies = forms.MultipleChoiceField(choices=(('Music', 'Music'), ('Movies', 'Movies'), ('Sports', 'Sports'), ('Travel', 'Travel')), required=False)
    photo = forms.ImageField(required=True)
    check = forms.BooleanField(required=True)
    cpi = forms.FloatField(required=True)  # New field for CPI
    resume = forms.FileField(required=True)  # New field for resume