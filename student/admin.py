from django.contrib import admin
from .models import Student,LeaveReportStudent,FeedbackStudent,NotificationStudent,StudentResult

admin.site.register(Student)
admin.site.register(LeaveReportStudent)
admin.site.register(FeedbackStudent)
admin.site.register(NotificationStudent)
admin.site.register(StudentResult)