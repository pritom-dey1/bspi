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
    SESSION_CHOICES = [
        ('25-26', '25-26'),
        ('24-25', '24-25'),
        ('23-24', '23-24'),
        ('22-23', '22-23'),
        ('21-22', '21-22'),
    ]

    DEPARTMENT_CHOICES = [
        ('CST', 'Computer Science & Tech'),
        ('ET', 'Electrical'),
        ('MT', 'Mechanical'),
        ('CMT', 'Civil'),
        ('AUT', 'Automobile'),
    ]

    WING_CHOICES = [
        ('Programming', 'Programming'),
        ('Graphics Design', 'Graphics Design'),
        ('Artificial Intelligence', 'Artificial Intelligence'),
        ('Cybersecurity', 'Cybersecurity'),
        ('IT and Hardware Support', 'IT and Hardware Support'),
    ]

    session = models.CharField(max_length=10, choices=SESSION_CHOICES)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    wing = models.CharField(max_length=100, choices=WING_CHOICES)
    is_email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    
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
    


class LeaderboardMember(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    image = models.ImageField(upload_to='leaderboard_images/')
    project_name = models.CharField(max_length=100)
    project_link = models.URLField()

    def __str__(self):
        return self.name
    
class LearningMaterial(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='learning_materials/')
    wing = models.CharField(max_length=100, choices=CustomUser.WING_CHOICES)
    content_link = models.URLField(blank=True) 

    def __str__(self):
        return self.title