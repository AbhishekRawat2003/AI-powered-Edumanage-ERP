from django.db import models
# from faculty.models import Faculty

class Course(models.Model):
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'course'  # Custom table name
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
class Session(models.Model):
    start_year = models.DateField()
    end_year = models.DateField()

    class Meta:
        db_table = 'session'  # Custom table name
        verbose_name = "Session"
        verbose_name_plural = "Sessions"
        ordering = ['-start_year']
    
    def __str__(self):
        return "From " + str(self.start_year) + " to " + str(self.end_year)
    

