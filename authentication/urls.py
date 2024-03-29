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
    path('logout/', views.logout_user, name='company_logout'),
    path('jobpost/', views.add_job_post, name='jobpost'),
    path('joblist/', views.job_list, name='joblist'),
    path('student-dashboard/', views.student_dashboard, name='student-dashboard'),
    path('apply_job/<int:job_id>/<str:company>/<str:position>/', apply_job, name='apply_job'),
    path('job_retrive/', views.job_retrive, name='job_retrive'),
    path('accept_reject_application/<int:application_id>/', views.accept_reject_application,
         name='accept_reject_application'),
    path('view',views.accepted_students,name='view'),
    path('download_excel/', views.download_excel, name='download_excel'),
    path('about/', views.about, name='about'),
    path('stop-job-opening/<int:job_post_id>/', stop_job_opening, name='stop_job_opening'),
    # Define the URL pattern for stop_job_opening
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)