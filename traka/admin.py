from django.contrib import admin

from traka.models import Profile

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'mobile', 'country', 'gender',]
