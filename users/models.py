from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField('First Name', max_length=255, blank=True,
                                  null=False)
    last_name = models.CharField('Last Name', max_length=255, blank=True,
                                 null=False)
    email = models.EmailField(unique=True)
    friends = models.ManyToManyField("self", verbose_name="list of friends", blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    def __str__(self):
        return self.email
