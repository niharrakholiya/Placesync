from django.conf.urls.static import static
from django.urls import path

from placesync import settings
from . import views
from .views import *

urlpatterns = [
    path("", views.home_page, name='home-page'),
    path("student-login/", views.student_login, name="student-login"),
    path("company-login/", views.company_login, name="company-login"),
    path("student-register/", views.register_student, name="student-register"),
    path("company-register/", views.register_company, name="company-register"),
    path("company-dashboard/", views.company_dashboard, name="company-dashboard"),
    path("companies/", views.companies, name="companies"),
    path('logout/', views.company_logout, name='company_logout')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)