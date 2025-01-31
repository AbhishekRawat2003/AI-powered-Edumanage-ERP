
from django.db import models
# from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
# >> NEW MODELS CREATED HERE......
from django.contrib.auth.models import AbstractUser
# from faculty.models import Faculty

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)
    def __str__(self) -> str:
       return super().__str__()

class CustomUser(AbstractUser):
    USER_TYPE = (
        (1, "HOD"),
        (2, "Staff"),
        (3, "Student")
    )

    GENDER = [
        ("M", "Male"),
        ("F", "Female")
        ]

    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(unique=True)
    user_type = models.IntegerField(default=1, choices=USER_TYPE)
    gender = models.CharField(max_length=1, choices=GENDER)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    address = models.TextField()
    fcm_token = models.TextField(default="")  # For firebase notifications
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    
    # Edited line
    def save(self, *args, **kwargs):
        # Hash the password before saving
        if self.pk is None or self.password:  # Only hash on creation or if password is updated
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        # Meta class to define options for this model
        db_table = 'custom_user'  # Custom table name
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
        ordering = ['-created_at']



