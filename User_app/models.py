# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

# models.py
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    gender = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=15)

    # Remove the custom related_name and use the default ones
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='customuser_set',
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='customuser_set',
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
