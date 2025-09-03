from django import forms
from .models import ContactMessage
from .models import CustomUser
import bleach
from .models import HelpPost ,LearningMaterial
from .models import LessonComment
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
class LessonCommentForm(forms.ModelForm):
    class Meta:
        model = LessonComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Add a comment...',
                'class': 'form-control'
            })
        }

class LearningMaterialForm(forms.ModelForm):
    class Meta:
        model = LearningMaterial
        fields = ['title', 'description', 'image', 'video', 'thumbnail', 'content_link', 'wing']
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'session', 'department', 'wing', 'is_leader', 'profile_pic')

class HelpPostForm(forms.ModelForm):
    class Meta:
        model = HelpPost
        fields = ['title', 'content', 'image']

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'session', 'department', 'wing', 'password']
        widgets = {
            'session': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'wing': forms.Select(attrs={'class': 'form-select'}),
        }
        help_texts = {
            'username': None, 
        }
        

# Reusable sanitize function
def clean_input(value):
    if value:
        return bleach.clean(value, tags=[], attributes={}, strip=True)
    return value


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'session', 'department', 'wing', 'is_leader', 'profile_pic')

    def clean_username(self):
        return clean_input(self.cleaned_data.get("username", ""))

    def clean_email(self):
        return clean_input(self.cleaned_data.get("email", ""))


class HelpPostForm(forms.ModelForm):
    class Meta:
        model = HelpPost
        fields = ['title', 'content', 'image']

    def clean_title(self):
        return clean_input(self.cleaned_data.get("title", ""))

    def clean_content(self):
        return clean_input(self.cleaned_data.get("content", ""))


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

    def clean_name(self):
        return clean_input(self.cleaned_data.get("name", ""))

    def clean_email(self):
        return clean_input(self.cleaned_data.get("email", ""))

    def clean_message(self):
        return clean_input(self.cleaned_data.get("message", ""))


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'session', 'department', 'wing', 'password']
        widgets = {
            'session': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'wing': forms.Select(attrs={'class': 'form-select'}),
        }
        help_texts = {
            'username': None, 
        }

    def clean_username(self):
        return clean_input(self.cleaned_data.get("username", ""))

    def clean_email(self):
        return clean_input(self.cleaned_data.get("email", ""))

    def clean_password(self):
        return clean_input(self.cleaned_data.get("password", ""))