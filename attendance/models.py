# from django.db import models
# # attendance/models.py


# # >> NEW MODELS CREATED HERE..............
# from course.models import Session
# from student.models import Student
# from faculty.models import Subject
# # from faculty.models import Faculty

# class Attendance(models.Model):
#     session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
#     subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
#     date = models.DateField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     class Meta:
#         db_table = 'attendance'  # Custom table name
#         verbose_name = "Attendance"
#         verbose_name_plural = "Attendances"
#         ordering = ['-date']

# class AttendanceReport(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
#     attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
#     status = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = 'attendance_report'  # Custom table name
#         verbose_name = "Attendance Report"
#         verbose_name_plural = "Attendance Reports"
#         ordering = ['student__admin__last_name']
#     def __str__(self):
#         return f"Attendance Report for {self.student.admin.first_name} {self.student.admin.last_name}"


from django.db import models
from course.models import Session
from student.models import Student
from faculty.models import Subject

class Attendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'attendance'  # Custom table name
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"
        ordering = ['-date']

    def __str__(self):
        return f"Attendance for {self.subject.name} on {self.date}"  # Added __str__ for Attendance model

class AttendanceReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'attendance_report'  # Custom table name
        verbose_name = "Attendance Report"
        verbose_name_plural = "Attendance Reports"
        ordering = ['student__admin__last_name']  # Assuming Student model has admin relationship

    def __str__(self):
        return f"Attendance Report for {self.student.admin.first_name} {self.student.admin.last_name}"
