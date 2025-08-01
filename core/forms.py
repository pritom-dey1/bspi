from django import forms
from .models import ContactMessage
from .models import CustomUser
from .models import HelpPost

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
        
