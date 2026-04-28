from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

# Create your models here.
EXPERIENCE_CHOICES = [('junior','Junior'), ('mid','Mid'), ('senior','Senior')]
USER_TYPE = [('candidate','Candidate'),('company','Company')]


#validaet username
def username_validator(username):
    for i in username:
        if not i.isalnum() and (i != '_') and (i != '-'):
            raise ValidationError('Allowed Characters in Username are A-Z, a-z, 1-9, _ , - ')
    if username.startswith('_') or username.endswith('_'):
        raise ValidationError('Username cant start or ends with Underscore.')
    if username.startswith('-') or username.endswith('-'):
        raise ValidationError('Username cant start or ends with -.')


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_no = PhoneNumberField(max_length=20, unique=True)
    user_type = models.CharField(max_length=9, choices=USER_TYPE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    username = models.SlugField(max_length=18, unique=True, db_index=True, validators=[username_validator])
    job_title = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    experience_level = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES, null=True, blank=True)
    experience_description = models.TextField(null=True, blank=True)
    resume = models.FileField(upload_to='resumes', null=True, blank=True)
    degree = models.CharField(max_length=50,null=True,blank=True)
    college_name = models.CharField(max_length=150,null=True, blank=True)
    university_name = models.CharField(max_length=150,null=True, blank=True)
    field_of_study = models.CharField(max_length=50,null=True, blank=True)
    projects = models.TextField(null=True, blank=True)
    school_name = models.CharField(max_length=150,null=True, blank=True)
    github_link = models.URLField(null=True, blank=True)
    linkedin_link = models.URLField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    company_username = models.SlugField(max_length=100, unique=True, db_index=True, validators=[username_validator])
    company_display_name = models.CharField(max_length=100)
    contact_email = models.EmailField(null=True, blank=True)
    contact_mobile_no = PhoneNumberField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    location= models.CharField(max_length=500)
    profile_picture = models.ImageField(upload_to='profile_pictures',null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    otp_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Companies'
