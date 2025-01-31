from django.db import models

# Create your models here.
from authentication.models import CustomUser
from course.models import Course
from course.models import Session
from faculty.models import Subject

# >> NEW MODELS CREATED HERE ...

class Student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'student'
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ['admin__last_name']
        
    def __str__(self):
        return self.admin.first_name + self.admin.last_name + ", " 
    
    
class LeaveReportStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'leave_report_student'
        verbose_name = "Leave Report Student"
        verbose_name_plural = "Leave Reports Students"
        ordering = ['-created_at']

    
class FeedbackStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'feedback_student'
        verbose_name = "Feedback Student"
        verbose_name_plural = "Feedbacks Students"
        ordering = ['-created_at']


class NotificationStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification_student'
        verbose_name = "Notification Student"
        verbose_name_plural = "Notifications Students"
        ordering = ['-created_at']

class StudentResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = models.FloatField(default=0)
    exam = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'student_result'
        verbose_name = "Student Result"
        verbose_name_plural = "Student Results"
        ordering = ['-created_at']