from django.contrib import admin

from authentication.models import Company, Student

# Register your models here.
admin.site.register(Company)
admin.site.register(Student)