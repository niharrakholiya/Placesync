import decimal
from pprint import pprint

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from .forms import StudentRegistrationForm, CompanyRegistrationForm, CompanyLoginForm, UserRegistrationForm, JobPostForm
from .forms import StudentLoginForm
from django.contrib.auth.hashers import make_password
from .models import Company, JobPost
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect

# Create your views here.


def home_page(request):
    return render(request, "index.html")


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
            # print("User:", user)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                print("It will be redirected")
                request.session['userid'] = user.company_profile.id
                print(user.company_profile.id)
                return redirect('company-dashboard')

            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = CompanyLoginForm()
    return render(request, 'company-login.html', {'form': form})

def company_logout(request):
    logout(request)
    return redirect('home-page')

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        user_form = UserRegistrationForm(request.POST)
        if form.is_valid() and user_form.is_valid():
            # Save student data
            student = form.save(commit=False)
            student.role = 'student'
            password = form.cleaned_data['password']
            hashed_password = make_password(password)
            student.password = hashed_password
            student.save()

            # Save user data
            user = user_form.save(commit=False)
            user.role = 'student'
            user.set_password(password)
            user.save()

            return redirect('student-login')
    else:
        form = StudentRegistrationForm()
        user_form = UserRegistrationForm()
    return render(request, 'student-register.html', {'form': form, 'user_form': user_form})


from .models import BasicUser

def register_company(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        company_name = request.POST.get('company_name')
        company_location = request.POST.get('company_location')
        company_link = request.POST.get('company_link')
        about = request.POST.get('about')
        company_image = request.FILES.get('company_image')

        # Create BasicUser object using CustomUserManager and save to database
        basic_user = BasicUser.objects.create_user(username=username, email=email, password=password)

        # Create Company object and associate it with the newly created BasicUser
        company = Company(
            user=basic_user,
            company_name=company_name,
            company_location=company_location,
            company_link=company_link,
            about=about,
            company_image=company_image
        )
        company.save()

        return redirect('company-login')
    else:
        return render(request, 'company-register.html')


@login_required(login_url='company-login')
def company_dashboard(request):

    user = request.user
    context = {}
    print(user)
    if hasattr(user, 'company_profile'):
        company = user.company_profile
        print(user.company_profile)
        print(company)  # Debug: Print company object
        recent_openings = JobPost.objects.filter(company=company)[:5]
        context = {
            'company': company,  # Pass the company object directly
            'recent_openings': recent_openings

        }
    return render(request, 'company-dashboard.html', context)


def companies(request):
    # Query all registered companies from the database
    # desired_image_url = None
    registered_companies = Company.objects.exclude(company_name="company")

    # Pass the registered companies to the template context
    context = {
        'registered_companies': registered_companies
    }

    # Render the HTML template with the provided context
    return render(request, 'companies.html', context)


def logout_user(request):
    logout(request)
    return redirect('home-page')


@login_required(login_url='company-login')
def add_job_post(request):
    if request.method == 'POST':
        company = Company.objects.get(id=request.session.get('userid'))
        # for data in company:
        #     print(data)
        print("company   ")
        print(company.id)
        salary = request.POST.get('salary')
        positions = request.POST.get('positions')
        location = request.POST.get('location')
        total_posts = request.POST.get('total_posts')

        print(salary, positions, location, total_posts)

        # Convert the salary value to a decimal
        # try:
        #     salary_decimal = decimal.Decimal(salary)
        # except decimal.InvalidOperation:
        #     # Handle the case where the input is not a valid decimal
        #     print("Invalid salary input")
        #     return
        #
        # # Convert the total_posts value to an integer
        # try:
        #     total_posts_int = int(total_posts)
        # except ValueError:
        #     # Handle the case where the input is not a valid integer
        #     print("Invalid total_posts input")
        #     return
        #
        # # Create the JobPost object
        print("you are printing job posts dear")
        jobpost = JobPost(
            company=company,
            salary=salary,
            positions=positions,
            location=location,
            total_posts=total_posts
        )
        print(jobpost)
        #
        # # Save the JobPost object
        try:
            jobpost.save()
            print("JobPost object saved successfully")
        except Exception as e:
            print(f"Error saving JobPost object: {e}")
        return redirect('company-dashboard')
    else:
        return render(request, 'job-post.html')


def jobs(request):
    # Retrieve recent job openings
    recent_openings = JobPost.objects.all()[:5]  # Retrieve the 5 most recent job openings
    context = {
        'recent_openings': recent_openings
    }
    return render(request, 'company-dashboard.html', context)
