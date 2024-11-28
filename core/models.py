from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    pass
    email = models.EmailField(unique=True, max_length=255) 
    username = models.CharField(unique=True, max_length=255)
    

