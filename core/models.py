from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

GENDER_CHOICE = (
    ('M', "Male"),
    ("F", "Female"),
    ("O", "Other")
)

MESSAGE_CHOICE = (
    ("NONE", "You are safe."),
    ("MILD", "You should take precautions."),
    ("MODERATE", "You should be home quarantine for 15 days."),
    ("SEVERE", "You should concern a doctor immediately.")
)

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, null=True)
    gender = models.CharField(choices=GENDER_CHOICE, max_length=1)
    age = models.IntegerField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'username', 'age', 'gender']


class PastDisease(models.Model):
    user = models.OneToOneField(
        to='User', on_delete=models.CASCADE, related_name='past_disease', related_query_name='past_disease')
    pneumonia = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    asthma = models.BooleanField(default=False)
    hypertension = models.BooleanField(default=False)
    cardiovascular = models.BooleanField(default=False)
    renal_chronic = models.BooleanField(default=False)
    tobacco = models.BooleanField(default=False)
    obesity = models.BooleanField(default=False)


class Report(models.Model):
    user = models.ForeignKey(
        to='User', on_delete=models.CASCADE, related_name='reports', related_query_name='reports')
    fever = models.BooleanField(default=False)
    tiredness = models.BooleanField(default=False)
    dry_cough = models.BooleanField(default=False)
    difficulty_in_breathing = models.BooleanField(default=False)
    sore_throat = models.BooleanField(default=False)
    pains = models.BooleanField(default=False)
    diarrhea = models.BooleanField(default=False)
    nasal_congestion = models.BooleanField(default=False)
    runny_nose = models.BooleanField(default=False)
    vulnerability_score = models.IntegerField(validators=[
        MaxValueValidator(10), MinValueValidator(0)])
    message = models.CharField(choices=MESSAGE_CHOICE, max_length=10)
    severity_level = models.IntegerField(validators=[
        MaxValueValidator(3), MinValueValidator(0)])
    date = models.DateTimeField(auto_now_add=True)
