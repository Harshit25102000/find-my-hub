from django.db import models
import pandas as pd
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
import pickle
from django.db.models import JSONField
import json
# Create your models here.

# User customization goes down

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    def __str__(self):
        return self.email

class people_info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coffee = models.CharField(max_length=10)
    cook = models.CharField(max_length=10)
    drink =models.CharField(max_length=10)
    eating_out = models.CharField(max_length=10)
    exercise= models.CharField(max_length=10)
    pay_meal = models.CharField(max_length=10)
    cluster=models.IntegerField(max_length=10,default=0)

class Dataframe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area=models.CharField(default="none",max_length=100)
    dataframe_binary = models.BinaryField()

    def set_dataframe(self, df):
        self.dataframe_binary = pickle.dumps(df)

    def get_dataframe(self):
        df = pickle.loads(self.dataframe_binary)
        return df

class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.TextField()
    longitude = models.TextField()

    def set_latitude(self, latitude):
        self.latitude = json.dumps(latitude)

    def get_latitude(self):
        return json.loads(self.latitude)

    def set_longitude(self, longitude):
        self.longitude = json.dumps(longitude)

    def get_longitude(self):
        return json.loads(self.longitude)