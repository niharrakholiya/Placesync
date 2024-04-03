from datetime import date

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class BasicUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=[('student', 'Student'), ('company', 'Company')], default='student')
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Student(models.Model):
    user = models.OneToOneField(BasicUser, on_delete=models.CASCADE, related_name='student_profile', default='')
    student_name = models.CharField(max_length=30, default="")

    GENDER_CHOICES = (
            ('Male', 'Male'),
            ('Female', 'Female')
        )

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    age = models.IntegerField(default=18)
    dob = models.DateField(default=date.today)
    email = models.EmailField(unique=True, null=True)
    phone_number = models.CharField(max_length=10, null=True)
    address = models.TextField(default="nothing")
    state = models.CharField(max_length=100, null=True)
    pincode = models.CharField(max_length=6, null=True)
    photo = models.ImageField(upload_to='static/student_photos/', null=True)
    resume = models.FileField(upload_to='static/student_resumes/', null=True, blank=True)
    cpi = models.FloatField(null=True, blank=True)


def get_default_company():
    try:
        company = Company.objects.get(company_name='company')
    except Company.DoesNotExist:
        # Generate a unique username for the default company user
        default_username = 'company'
        index = 1
        while BasicUser.objects.filter(username=default_username).exists():
            default_username = f'company{index}'
            index += 1

        # Generate a unique email address for the default company user
        default_email = 'company@example.com'
        index = 1
        while BasicUser.objects.filter(email=default_email).exists():
            default_email = f'company{index}@example.com'
            index += 1

        user = BasicUser.objects.create(username=default_username, email=default_email, is_staff=True, is_superuser=True)
        company = Company.objects.create(user=user, company_name='company')
    return company



class Company(models.Model):
    user = models.OneToOneField(BasicUser, on_delete=models.CASCADE, related_name='company_profile', default=get_default_company)
    company_name = models.CharField(max_length=255, default='')  # Add company name field
    company_location = models.CharField(max_length=255, default='')  # Add company location field
    company_image = models.ImageField(upload_to='company_images/', null=True, blank=True)  # Add image field
    company_link = models.URLField(blank=True)  # Add company link field
    about = models.TextField(blank=True)  # Add about field

    from django.db import models
    from django.contrib.auth.models import User

class JobPost(models.Model):
        company = models.ForeignKey(Company, on_delete=models.CASCADE)  # Assuming Company is linked to User
        total_posts = models.IntegerField()
        positions = models.CharField(max_length=100)
        salary = models.DecimalField(max_digits=10, decimal_places=2)
        location = models.CharField(max_length=100)
        active = models.BooleanField(default=True)  # Add a field to indicate if the job opening is active

        def __str__(self):
            return f"{self.positions} at {self.location}"


class JobApplication(models.Model):
    # Other fields
    job_id = models.IntegerField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Assuming Student is the name of the Student model
    company = models.CharField(max_length=100)  # Field to store the name of the company
    position = models.CharField(max_length=100)  # Field to store the position applied for

    def __str__(self):
        return f"{self.student.student_name} - {self.company} - {self.position}"


from django.db import models
from django.utils.translation import gettext_lazy as _

class ApplicationStatus(models.Model):
    ACCEPTED = 'AC'
    REJECTED = 'RE'

    STATUS_CHOICES = [
        (ACCEPTED, _('Accepted')),
        (REJECTED, _('Rejected')),
    ]

    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    student_name = models.CharField(max_length=100)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    is_accepted = models.BooleanField(default=False)  # New field to mark if the student is accepted

    def __str__(self):
        return f"{self.student_name} - {self.status}"
