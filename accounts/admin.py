from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Profile, VerificationCode,IpAdress

@admin.register(Profile)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')


@admin.register(VerificationCode)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime_created', 'code')


@admin.register(IpAdress)
class IpAddress(admin.ModelAdmin):
    list_display = ('ip', 'datetime_created')