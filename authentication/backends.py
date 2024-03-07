# from django.contrib.auth.backends import BaseBackend
# from .models import Student, Company
#
#
# class CustomAuthBackend(BaseBackend):
#     def authenticate(self, request, username=None, password=None):
#         # Check if the username is a student username
#         try:
#             student = Student.objects.get(username=username)
#             if student.check_password(password):
#                 return student
#         except Student.DoesNotExist:
#             pass
#
#         # Check if the username is a company username
#         try:
#             company = Company.objects.get(username=username)
#             if company.check_password(password):
#                 return company
#         except Company.DoesNotExist:
#             pass
#
#         # Check if the username is a student email
#         try:
#             student = Student.objects.get(email=username)
#             if student.check_password(password):
#                 return student
#         except Student.DoesNotExist:
#             pass
#
#     def get_user(self, user_id):
#         try:
#             return Student.objects.get(pk=user_id)
#         except Student.DoesNotExist:
#             try:
#                 return Company.objects.get(pk=user_id)
#             except Company.DoesNotExist:
#                 return None
