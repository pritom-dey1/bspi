import random
from django.core.mail import send_mail

def generate_verification_code():
    return str(random.randint(100000, 999999))

def send_verification_email(email, code):
    subject = '🔒 Email Verification Code'
    plain_message = f'Your verification code is: {code}' 
    from_email = 'noreply@bspi.com'
    recipient_list = [email]

    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
            <h2 style="text-align: center; color: #333;">🔐 Email Verification</h2>
            <p style="font-size: 16px; color: #555;">
                Hello,
                <br><br>
                Thank you for registering with us. Please use the following verification code to verify your email address:
            </p>
            <div style="text-align: center; margin: 30px 0;">
                <span style="display: inline-block; font-size: 24px; font-weight: bold; background: #007bff; color: white; padding: 15px 30px; border-radius: 8px;">
                    {code}
                </span>
            </div>
            <p style="font-size: 14px; color: #999; text-align: center;">
                This code will expire in 10 minutes. If you did not request this, please ignore this email.
            </p>
        </div>
    </body>
    </html>
    """

    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
