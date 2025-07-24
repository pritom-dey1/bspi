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
    is_approved = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    def __str__(self):
        return self.username
    
    

class Event(models.Model):
    title = models.CharField(max_length=200)                  # Event er title
    description = models.TextField()                           # Event er details ba description
    main_image = models.ImageField(upload_to='events/', blank=True, null=True)  # Main banner image (optional)
    created_at = models.DateTimeField(default=timezone.now)   # Created date/time

    def __str__(self):
        return self.title
    
    
class EventMomentImage(models.Model):
    event = models.ForeignKey(Event, related_name='moments', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_moments/')
    caption = models.CharField(max_length=200, blank=True, null=True)  # optional

    def __str__(self):
        return f"Moment for {self.event.title}"
    
    

class Person(models.Model):
    ROLE_CHOICES = [
        ('advisor', 'Advisor'),
        ('executive', 'Executive Board'),
        ('general', 'General Member'),
    ]

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    position = models.CharField(max_length=100, blank=True)  # e.g., Tech Team Lead
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='profiles/')
    linkedin = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.role})"