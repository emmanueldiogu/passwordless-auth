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

    country = models.CharField(max_length=60)
    language = models.CharField(max_length=60)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default=GENDER_MALE)
    height = models.DecimalField(max_digits=6, decimal_places=2)
    height_unit = models.CharField(
        max_length=2, choices=HEIGHT_UNITS_CHOICES, default=HEIGHT_UNITS_CM)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    weight_unit = models.CharField(
        max_length=2, choices=WEIGHT_UNITS_CHOICES, default=WEIGHT_UNITS_KG)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        # ordering = ['first_name', 'last_name']
        pass
