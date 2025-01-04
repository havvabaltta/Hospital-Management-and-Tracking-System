from django.db import models
from django.contrib.auth.models import AbstractUser

class Admin(AbstractUser):
    is_admin = models.BooleanField(default=True)

class Doctor(AbstractUser):
    is_doctor = models.BooleanField(default=True)

class Patient(AbstractUser):
    is_patient = models.BooleanField(default=True)
