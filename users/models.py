from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_ROLES = (
        ('donor', 'Donor'),
        ('recipient', 'Recipient/Hospital'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=USER_ROLES, default='donor')
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)


# Create your models here.
