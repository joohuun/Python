from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(blank=False, unique=True)

    EMAIL_FIELD = 'email'

    USERNAME_FIELD = 'username'
