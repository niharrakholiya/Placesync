# authentication/backends.py

from django.contrib.auth.backends import BaseBackend
from .models import Student, Company


class StudentBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            student = Student.objects.get(username=username)
            if student.check_password(password):
                return student
        except Student.DoesNotExist:
            pass
        return None

class CompanyBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            company = Company.objects.get(username=username)
            if company.check_password(password):
                return company
        except Company.DoesNotExist:
            pass
        return None
