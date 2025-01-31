from django.contrib import admin

from .models import Attendance,AttendanceReport

admin.site.register(Attendance)
admin.site.register(AttendanceReport)