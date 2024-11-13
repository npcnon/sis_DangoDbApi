#users.models

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    student_id = models.CharField(max_length=12, unique=True, null=True, blank=True)
    fulldata_applicant_id = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    username = None


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)