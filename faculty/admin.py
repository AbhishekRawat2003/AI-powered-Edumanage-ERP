from django.contrib import admin

from faculty.models import Faculty,Subject,LeaveReportFaculty,FeedbackFaculty,NotificationFaculty,Admin


admin.site.register(Faculty)
admin.site.register(Subject)
admin.site.register(LeaveReportFaculty)
admin.site.register(FeedbackFaculty)
admin.site.register(NotificationFaculty)
admin.site.register(Admin)

