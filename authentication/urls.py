from django.urls import path
from . import views
from .views import *
urlpatterns = [
path("", views.home_page, name='home-page'),
path("student-login/", views.student_login, name="student-login"),
path("company-login/", views.company_login, name="company-login"),
path("student-register/", views.register_student, name="student-register"),
]