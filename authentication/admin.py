from django.contrib import admin

from authentication.models import Company, Student, BasicUser

# Register your models here.
admin.site.register(Company)
admin.site.register(Student)
admin.site.register(BasicUser)
