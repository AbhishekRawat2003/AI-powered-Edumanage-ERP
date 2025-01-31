# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,CustomUserManager


# admin.site.register(CustomUserManager)
# admin.site.register(CustomUser)

from django.contrib import admin

admin.site.register(CustomUser)
