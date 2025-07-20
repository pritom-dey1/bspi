from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='announcements/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    # Optional question by user
    question = models.TextField(blank=True, null=True)

    # Admin answer
    answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
    
from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
    
    
    

class CustomUser(AbstractUser):
    SEMESTER_CHOICES = [
        ('1st', '1st'),
        ('2nd', '2nd'),
        ('3rd', '3rd'),
        ('4th', '4th'),
        ('5th', '5th'),
        ('6th', '6th'),
        ('7th', '7th'),
        ('8th', '8th'),
    ]

    DEPARTMENT_CHOICES = [
        ('CST', 'Computer Science & Tech'),
        ('ET', 'Electrical'),
        ('MT', 'Mechanical'),
        ('CMT', 'Civil'),
    ]

    WING_CHOICES = [
        ('Programming', 'Programming'),
        ('Graphics Design', 'Graphics Design'),
        ('Artificial Intelligence', 'Artificial Intelligence'),
        ('Cybersecurity', 'Cybersecurity'),
    ]

    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    wing = models.CharField(max_length=100, choices=WING_CHOICES)
    is_email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    
    # New field to identify leader or member
    is_leader = models.BooleanField(default=False)

    def __str__(self):
        return self.username