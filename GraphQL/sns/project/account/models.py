from django.db import models
from django.contrib.auth.models import AbstractUser
from ..models import BaseModel
# Create your models here.

class User(AbstractUser, BaseModel):
    email = models.EmailField(blank=False, unique=True)

    EMAIL_FIELD = 'email'

    USERNAME_FIELD = 'username'
