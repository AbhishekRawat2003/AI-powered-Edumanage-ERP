from django.contrib import admin
from .models import Course,Session

admin.site.register(Session)
admin.site.register(Course)