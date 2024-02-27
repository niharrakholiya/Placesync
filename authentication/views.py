from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.core.checks import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentRegistrationForm
from .forms import StudentLoginForm
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
            print(username)
            print(password)
            print(make_password(password))
            user = authenticate(request, username="aabbaa", password="pbkdf2_sha256$720000$B569yMy5ZzH20BKLFLWEgQ$m4eNHOWPNDdqoPmjO/k7sz31tlhbG/ihTP1ix7OEH2Y=")
            print("User:", user)
            if user is not None:
                print(check_password("aabbaa", user.password))
                if check_password(password, user.password):  # Check hashed password
                    login(request, user)
                    messages.success(request, 'Login successful.')
                    return redirect('home-page')
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
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            print("Entered email:", username)
            print("Entered password:", password)
            user = authenticate(username=username, password=password)
            if user is  None:
                messages.info(request, 'Incorrect Password.')
                return redirect('tpo-login')
            login(request, user)

            messages.success(request, 'Successfully logged in')
            return redirect('tpo-dashboard')
    except Exception as e:
        print(e)
    return render(request, "company-login.html")

from django.contrib.auth.hashers import make_password

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
