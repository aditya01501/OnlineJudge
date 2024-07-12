from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    can_create = models.BooleanField(default=False)
    #USERNAME_FIELD = ['username']
# Create your models here.
