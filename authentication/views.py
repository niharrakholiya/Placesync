from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from .forms import StudentRegistrationForm, CompanyRegistrationForm, CompanyLoginForm
from .forms import StudentLoginForm
from django.contrib.auth.hashers import make_password


# Create your views here.

def home_page(request):
    return render(request, "index.html")


from django.contrib.auth.hashers import check_password


def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            print("User:", user)
            if user is not None:
                if check_password(password, user.password):  # Check hashed password
                    login(request, user)
                    messages.success(request, 'Login successful.')
                    return redirect('test')
                else:
                    messages.error(request, 'Invalid username or password.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = StudentLoginForm()
    return render(request, 'student-login.html', {'form': form})


def company_login(request):
    if request.method == 'POST':
        form = CompanyLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            print("User:", user)
            if user is not None and user.is_active:
                    login(request, user)
                    messages.success(request, 'Login successful.')
                    print("It will be redirected")
                    return redirect('company-dashboard')

            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = CompanyLoginForm()
    return render(request, 'company-login.html', {'form': form})


def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Get the unsaved user object
            password = form.cleaned_data['password']  # Get the raw password from the form
            hashed_password = make_password(password)  # Hash the password
            user.password = hashed_password
            user.save()  # Save the user object with the hashed password
            return redirect('student-login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'student-register.html', {'form': form})


def register_company(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            hashed_password = make_password(password)
            user.password = hashed_password
            # Additional fields from the form
            user.email = form.cleaned_data['email']
            user.company_name = form.cleaned_data['company_name']
            user.company_location = form.cleaned_data['company_location']
            user.save()
            return redirect('company-login')
    else:
        form = CompanyRegistrationForm()
    return render(request, 'company-register.html', {'form': form})


@login_required(login_url='company-login')
def company_dashboard(request):
    company = request.user  # Assuming the logged-in user is a Company instance
    print(company)
    return render(request, 'company-dashboard.html')
    pass
