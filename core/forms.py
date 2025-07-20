from django import forms
from .models import ContactMessage
from .models import CustomUser


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'semester', 'department', 'wing', 'password']
        widgets = {
            'semester': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'wing': forms.Select(attrs={'class': 'form-select'}),
        }
        help_texts = {
            'username': None, 
        }
        
