from django.db import models
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.
class user(models.Model):
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    username = models.CharField(max_length=50, null=False, blank=False, unique=True)
    email = models.EmailField(max_length=128, null=False, blank=False)
    password = models.CharField(max_length=50, null=False,blank=False)
    dob = models.DateField(null=True, blank=True)
    isActive = models.BooleanField(default=False)
    isVerify = models.BooleanField(default=False)
    verify_code = models.CharField(max_length=10, null=False,blank=False)

    