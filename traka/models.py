from django.db import models
from django.contrib import admin
from django.contrib.auth import get_user_model

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='user_profile')
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_OTHERS = 'O'

    GENDER_CHOICES = [
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHERS, 'Others'),
    ]

    WEIGHT_UNITS_KG = 'kg'
    WEIGHT_UNITS_PNDS = 'lb'

    WEIGHT_UNITS_CHOICES = [
        (WEIGHT_UNITS_KG, 'kilogram'),
        (WEIGHT_UNITS_PNDS, 'pounds'),
    ]

    HEIGHT_UNITS_CM = 'cm'
    HEIGHT_UNITS_FT = 'ft'

    HEIGHT_UNITS_CHOICES = [
        (HEIGHT_UNITS_CM, 'centimeters'),
        (HEIGHT_UNITS_FT, 'feets'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=60)
    language = models.CharField(max_length=60)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default=GENDER_MALE)
    height = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    height_unit = models.CharField(
        max_length=2, choices=HEIGHT_UNITS_CHOICES, default=HEIGHT_UNITS_CM)
    weight = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    weight_unit = models.CharField(
        max_length=2, choices=WEIGHT_UNITS_CHOICES, default=WEIGHT_UNITS_KG)

    def __str__(self) -> str:
        return self.user.email

    @admin.display(ordering='user__email')
    def email(self):
        return self.user.email

    @admin.display(ordering='user__mobile')
    def mobile(self):
        return self.user.mobile

    class Meta:
        ordering = ['first_name', 'last_name', 'user__email', 'user__mobile', 'country', 'gender']

class StepCounter(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='user_step', null=True, blank=True)
    uuid = models.CharField(max_length=255, blank=True, null=True)
    counts = models.IntegerField()
    
class ActivitiesLog(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='user_activity', null=True, blank=True)
    uuid = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=250, null=True, blank=True)
    Screen = models.CharField(max_length=250, null=True, blank=True)
    Product = models.IntegerField(null=True, blank=True)
    
    
    
