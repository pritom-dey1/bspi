from django.shortcuts import render
from .models import Announcement
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from .models import CustomUser
from .utils import generate_verification_code, send_verification_email
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def post_login_redirect(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            return redirect('leader_dashboard')  # or admin dashboard
        else:
            return redirect('user_dashboard')
    else:
        return redirect('login')

def home(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Thanks! Your message has been received.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    form = ContactForm()
    return render(request, 'home.html', {'form': form})

def announcement_page(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'announcement.html', {'announcements': announcements})



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            code = generate_verification_code()
            user.verification_code = code
            user.set_password(form.cleaned_data['password'])
            user.is_active = False  # inactive until verify
            user.save()
            send_verification_email(user.email, code)
            request.session['email'] = user.email  # save email in session
            return redirect('verify')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def verify(request):
    email = request.session.get('email')
    if not email:
        return redirect('register')

    user = CustomUser.objects.filter(email=email).first()
    if not user:
        return redirect('register')

    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        print(f"Entered: {code} | Expected: {user.verification_code}")

        if code == user.verification_code:
            user.is_active = True
            user.is_email_verified = True
            user.verification_code = ''
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'verify.html', {'error': 'Invalid code'})

    return render(request, 'verify.html')

from django.contrib.auth.decorators import login_required

@login_required
def post_login_redirect(request):
    user = request.user
    if user.is_leader:
        return redirect('leader_dashboard')
    return redirect('user_dashboard')  # সাধারণ member এর জন্য


@login_required
def leader_dashboard(request):
    user = request.user
    if not user.is_leader:
        return redirect('home')  # সিকিউরিটি purposes

    # Leader এর wing এর সকল user
    members = CustomUser.objects.filter(
        wing=user.wing,
        is_leader=False
    )
    return render(request, 'leader_dashboard.html', {
        'members': members,
        'wing': user.wing
    })


@login_required
def user_dashboard(request):
    return render(request, 'user_dashboard.html')


@login_required
def learning_page(request):
    return render(request, 'learning.html') 


def redirect_learning(request):
    if request.user.is_authenticated:
        return redirect('learning')
    else:
        return redirect('login')