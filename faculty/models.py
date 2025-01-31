from django.db import models

# >> NEW MODELS CREATED HERE ......
from authentication.models import CustomUser
from course.models import Course
from django.dispatch import receiver
from django.db.models.signals import post_save


class Faculty(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    class Meta:
        db_table = 'faculty'  # Custom table name
        verbose_name = "Faculty"
        verbose_name_plural = "Faculties"
        ordering = ['admin__last_name']

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name

class Subject(models.Model):
    name = models.CharField(max_length=120)
    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE,)
    course = models.ForeignKey(Course,related_name = 'subjects', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'subject'
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        ordering = ['name']

    def __str__(self):
        return self.name

class LeaveReportFaculty(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leave_report_faculty'
        verbose_name = "Leave Report Faculty"
        verbose_name_plural = "Leave Reports Faculty"
        ordering = ['-created_at']

class FeedbackFaculty(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'feedback_sfaculty'
        verbose_name = "Feedback Faculty"
        verbose_name_plural = "Feedbacks Faculty"
        ordering = ['-created_at']


class NotificationFaculty(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification_faculty'
        verbose_name = "Notification Faculty"
        verbose_name_plural = "Notifications Faculty"
        ordering = ['-created_at']
    
class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    class Meta:
        db_table = 'admin'
        verbose_name = "Administrator"
        verbose_name_plural = "Administrators"
        ordering = ['admin__last_name']


@receiver(post_save,sender=CustomUser)
def Create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Faculty.objects.create(admin=instance)
        if instance.user_type == 3:
            Faculty.objects.create(admin=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    # Save related Admin, Faculty, or Student profile based on user_type
    if instance.user_type == 1:  # HOD
        if hasattr(instance, 'admin'):
            instance.admin.save()
    elif instance.user_type == 2:  # Faculty
        if hasattr(instance, 'faculty'):
            instance.faculty.save()
    elif instance.user_type == 3:  # Student
        if hasattr(instance, 'student'):
            instance.student.save()