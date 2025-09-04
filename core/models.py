from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class HelpPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='helppost_images/', blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(HelpPost, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
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
    title = models.CharField(max_length=200)                  
    description = models.TextField()                           
    main_image = models.ImageField(upload_to='events/', blank=True, null=True)  
    created_at = models.DateTimeField(default=timezone.now)   

    def __str__(self):
        return self.title
    
    
class EventMomentImage(models.Model):
    event = models.ForeignKey(Event, related_name='moments', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_moments/')
    caption = models.CharField(max_length=200, blank=True, null=True) 

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
    position = models.CharField(max_length=100, blank=True)  
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
    video = models.FileField(upload_to='learning_videos/', blank=True, null=True)  # New video field
    thumbnail = models.ImageField(upload_to='learning_thumbnails/', blank=True, null=True)  # Optional thumbnail
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.title
    
class QuizQuestion(models.Model):
    lesson = models.ForeignKey(LearningMaterial, on_delete=models.CASCADE, related_name="quizzes")
    question = models.CharField(max_length=300)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_answer = models.CharField(
        max_length=200,
        choices=[
            ("option1", "Option 1"),
            ("option2", "Option 2"),
            ("option3", "Option 3"),
            ("option4", "Option 4"),
        ]
    )

    def __str__(self):
        return f"{self.lesson.title} - {self.question}"
    
    
class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(LearningMaterial, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lesson') 

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} ({self.score}/{self.total})"



class LessonComment(models.Model):
    lesson = models.ForeignKey(LearningMaterial, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.lesson.title}"