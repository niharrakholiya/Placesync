from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.db import models


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


class BasicUser(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=[('student', 'Student'), ('company', 'Company')], default='student')
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Student(models.Model):
    user = models.OneToOneField(BasicUser, on_delete=models.CASCADE, related_name='student_profile',default='')
    # Add student-specific fields here
from django.contrib.auth import get_user_model

User = get_user_model()


def get_default_company_user():
    try:
        user = User.objects.get(username='company')
    except User.DoesNotExist:
        user = User.objects.create(username='company', email='company@example.com', is_staff=True)
    return user


class Company(models.Model):
    user = models.OneToOneField(BasicUser, on_delete=models.CASCADE, related_name='company_profile',default=get_default_company_user)
    company_name = models.CharField(max_length=255, default='')  # Add company name field
    company_location = models.CharField(max_length=255, default='')  # Add company location field
    company_image = models.ImageField(upload_to='company_images/', null=True, blank=True)  # Add image field
    company_link = models.URLField(blank=True)  # Add company link field
    about = models.TextField(blank=True)  # Add about field