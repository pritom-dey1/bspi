import random
from django.core.mail import send_mail

def generate_verification_code():
    return str(random.randint(100000, 999999))

def send_verification_email(email, code):
    subject = 'Your Verification Code'
    message = f'Your verification code is: {code}'
    from_email = 'noreply@bspi.com'
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)
