from django.shortcuts import render, get_object_or_404
from .models import Announcement
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactForm
from django.views.decorators.http import require_POST
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import HelpPostForm
from django.conf import settings  
from django.core.mail import send_mail
from .forms import RegistrationForm
from .models import CustomUser ,QuizAttempt
from .models import Event
from .utils import generate_verification_code, send_verification_email
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Person
from .models import LeaderboardMember
from .models import LearningMaterial
from django.contrib.auth.views import LoginView
from axes.helpers import get_client_ip_address
from axes.handlers.proxy import AxesProxyHandler
from django.contrib import messages
import bleach
import json
from .models import HelpPost, Comment ,QuizQuestion
from .forms import HelpPostForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch

@login_required
def download_quiz_pdf(request, lesson_id):
    lesson = get_object_or_404(LearningMaterial, id=lesson_id)
    attempt = QuizAttempt.objects.filter(user=request.user, lesson=lesson).first()
    questions = QuizQuestion.objects.filter(lesson=lesson)

    if not attempt:
        return HttpResponse("No quiz attempt found.", status=404)

    # HTTP Response for PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{lesson.title}_quiz_result.pdf"'

    # PDF document
    doc = SimpleDocTemplate(response, pagesize=A4,
                            rightMargin=30, leftMargin=30,
                            topMargin=30, bottomMargin=30)

    story = []
    styles = getSampleStyleSheet()

    # Custom Styles
    title_style = ParagraphStyle(
        "title",
        parent=styles["Heading1"],
        fontSize=20,
        alignment=1,  # center
        textColor=colors.HexColor("#0d47a1"),  # deep blue
        spaceAfter=20,
    )
    normal_style = styles["Normal"]

    # Header
    story.append(Paragraph("BSPI COMPUTER CLUB", title_style))
    story.append(Paragraph(f"Quiz Result for <b>{lesson.title}</b>", normal_style))
    story.append(Paragraph(f"Student: <b>{request.user.username}</b>", normal_style))
    story.append(Paragraph(f"Score: <b>{attempt.score}</b> / {attempt.total}", normal_style))
    story.append(Spacer(1, 0.3 * inch))

    # Table data (NO 'Your Answer' column)
    data = [["#", "Question", "Options", "Correct Answer"]]

    for i, q in enumerate(questions, start=1):
        options = f"a) {q.option1}<br/>b) {q.option2}<br/>c) {q.option3}<br/>d) {q.option4}"
        correct = getattr(q, q.correct_answer)

        data.append([
            str(i),
            Paragraph(q.question, normal_style),
            Paragraph(options, normal_style),
            Paragraph(correct, normal_style),
        ])

    # Table formatting
    table = Table(data, colWidths=[30, 180, 200, 140])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1565c0")),  # Header bg
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOX", (0, 0), (-1, -1), 1, colors.black),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    story.append(table)
    doc.build(story)
    return response

@login_required
def help_section(request):
    if request.method == 'POST':
        form = HelpPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('help_section')
    else:
        form = HelpPostForm()

    posts = HelpPost.objects.all().order_by('-created_at').prefetch_related('comments')
    return render(request, 'help_section.html', {'form': form, 'posts': posts})

@csrf_exempt
def create_post(request):
    if request.method == 'POST':    
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        user = request.user

        if not user.is_authenticated:
            return JsonResponse({'error': 'Not authenticated'}, status=401)

        post = HelpPost.objects.create(user=user, title=title, content=content, image=image)

        return JsonResponse({'message': 'Post created', 'post_id': post.id}, status=201)

@require_POST
@login_required
def create_comment(request):
    try:
        content = request.POST.get('content', '').strip()
        post_id = request.POST.get('post_id')

        if not post_id or not content:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Missing post ID or content.'}, status=400)
            else:
                return redirect('help_section')

        post = get_object_or_404(HelpPost, id=post_id)

        comment = Comment.objects.create(
            user=request.user,
            post=post,
            content=content
        )

        # AJAX response
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'username': request.user.username,
                'content': comment.content
            }, status=201)

        return redirect('help_section')
    
    except Exception as e:
        print("Error in create_comment:", str(e))  # for debugging
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Server error'}, status=500)
        return redirect('help_section')

def get_posts(request):
    posts_data = []
    for post in HelpPost.objects.all().order_by('-created_at'):
        comments = post.comments.all()
        posts_data.append({
            'id': post.id,
            'user': post.user.username,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M'),
            'image_url': post.image.url if post.image else None,
            'comments': [
                {'user': c.user.username, 'content': c.content, 'created_at': c.created_at.strftime('%Y-%m-%d %H:%M')}
                for c in comments
            ]
        })
    return JsonResponse({'posts': posts_data})

def clean_input(text):
    allowed_tags = []  # kono tag allow korben na
    allowed_attrs = {}
    return bleach.clean(text, tags=allowed_tags, attributes=allowed_attrs, strip=True)
class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        username = request.POST.get('username') if request.method == "POST" else None
        credentials = {'username': username} if username else None
        
        locked = AxesProxyHandler.is_locked(request, credentials=credentials)
        
        if locked:
            return render(request, 'blocked.html', status=403)
        return super().dispatch(request, *args, **kwargs)

def about_page(request):
        advisors = Person.objects.filter(role='advisor')
        executives = Person.objects.filter(role='executive')
        generals = Person.objects.filter(role='general')[:5]
        
        return render(request, 'about.html', {
            'advisors': advisors,
            'executives': executives,
            'generals': generals,
        })
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Optional: to disable login
            user.is_approved = False  # Must be approved by leader
            user.save()

            messages.success(request, "Registration successful! Wait for leader approval.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})
def post_login_redirect(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            return redirect('leader_dashboard')  # or admin dashboard
        else:
            return redirect('user_dashboard')
    else:
        return redirect('login')

def home(request):
    members = LeaderboardMember.objects.all()[:5]
    latest_event = Event.objects.order_by('-created_at').first()

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Thanks! Your message has been received.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    form = ContactForm()
    return render(request, 'home.html', {
        'form': form,
        'members': members,
        'latest_event': latest_event,
    })
def announcement_page(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'announcement.html', {'announcements': announcements})

def announcement_detail(request, id):
    announcement = get_object_or_404(Announcement, id=id)
    return render(request, 'announcement_detail.html', {'announcement': announcement})


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

def create_help_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')  # ✅ handle uploaded image

        HelpPost.objects.create(user=request.user, title=title, content=content, image=image)
        return redirect('help_section')  # redirect to post list

    return render(request, 'help_post_create.html')

def verify(request):
    email = request.session.get('email')
    if not email:
        return redirect('register')

    user = CustomUser.objects.filter(email=email).first()
    if not user:
        return redirect('register')

    if request.method == 'POST':
        code = request.POST.get('code', '').strip()

        if code == user.verification_code:
            user.is_email_verified = True
            user.verification_code = ''
            user.save()

            if user.is_approved:
                user.is_active = True
                user.save()
                login(request, user)
                return redirect('post_login_redirect')
            else:
                return render(request, 'pending_approval.html')  # Not approved yet
        else:
            return render(request, 'verify.html', {
                'error': '❌ Invalid verification code. Please try again.'
            })

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
        return redirect('home')

    # Approved members under this leader
    approved_members = CustomUser.objects.filter(
        wing=user.wing,
        is_leader=False,
        is_approved=True
    )

    # Pending members under this leader (awaiting approval)
    pending_members = CustomUser.objects.filter(
        wing=user.wing,
        is_leader=False,
        is_approved=False
    )

    return render(request, 'leader_dashboard.html', {
        'approved_members': approved_members,
        'pending_members': pending_members,
        'wing': user.wing,
    })

@require_POST
@login_required
def approve_member(request, user_id):
    if not request.user.is_leader:
        return redirect('home')

    member = CustomUser.objects.get(id=user_id, wing=request.user.wing)
    member.is_approved = True
    member.is_active = True  # enable login
    member.save()

    # ✅ Send email notification
    subject = "🎉 You're Approved to Login - BSPI Computer Club"
    message = f"Hi {member.username},\n\nYour account has been approved by your leader. You can now log in and access the system.\n\nGo to: https://your-domain.com/login\n\nThanks,\nBSPI Computer Club"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [member.email]

    try:
        send_mail(subject, message, from_email, recipient_list)
        messages.success(request, f"{member.username} has been approved and notified via email.")
    except:
        messages.warning(request, f"{member.username} has been approved, but email sending failed.")

    return redirect('leader_dashboard')
@login_required
def user_dashboard(request):
    user_wing = request.user.wing
    lessons = LearningMaterial.objects.filter(wing=user_wing)
    return render(request, 'user_dashboard.html', {
        'lessons': lessons
    })

@login_required
def learning_page(request):
    return render(request, 'learning.html') 


class ApprovalCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_approved:
            messages.warning(request, "Your account is not yet approved.")
            return redirect('logout')
        return self.get_response(request)
def redirect_learning(request):
    if request.user.is_authenticated:
        return redirect('learning')
    else:
        return redirect('login')
    
    
def event_list(request):
    events = Event.objects.all().order_by('-created_at')
    return render(request, 'event.html', {'events': events})





def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    return render(request, 'event_detail.html', {'event': event})
class ApprovalCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated:
            if not request.user.is_approved:
                messages.warning(request, "❌ Your account is pending leader approval.")
                from django.contrib.auth import logout
                logout(request)
                return redirect('login')
        return self.get_response(request)
    
@login_required
def learning_page(request):
    lessons = LearningMaterial.objects.filter(wing=request.user.wing)
    return render(request, 'learning.html', {'lessons': lessons})



@login_required
def quiz_page(request, lesson_id):
    lesson = get_object_or_404(LearningMaterial, id=lesson_id)
    questions = QuizQuestion.objects.filter(lesson=lesson)

    attempt = QuizAttempt.objects.filter(user=request.user, lesson=lesson).first()

    if attempt:
        percentage = (attempt.score / attempt.total) * 100 if attempt.total > 0 else 0
        return render(request, "quiz_result.html", {
            "lesson": lesson,
            "score": attempt.score,
            "total": attempt.total,
            "percentage": percentage,
            "already_done": True
        })

    if request.method == "POST":
        score = 0
        total = questions.count()

        for question in questions:
            selected = request.POST.get(str(question.id))
            if selected == getattr(question, "correct_answer"):
                score += 1

        attempt = QuizAttempt.objects.create(
            user=request.user,
            lesson=lesson,
            score=score,
            total=total
        )

        percentage = (score / total) * 100 if total > 0 else 0

        return render(request, "quiz_result.html", {
            "lesson": lesson,
            "score": score,
            "total": total,
            "percentage": percentage,
            "already_done": False
        })

    return render(request, "quiz.html", {"lesson": lesson, "questions": questions})

@login_required
def lesson_video_page(request, lesson_id):
    main_video = get_object_or_404(LearningMaterial, id=lesson_id)
    
    # Optional: related videos, same wing, exclude main
    related_videos = LearningMaterial.objects.filter(
        wing=request.user.wing
    ).exclude(id=lesson_id)

    # Pagination optional
    from django.core.paginator import Paginator
    paginator = Paginator(related_videos, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'lession_vd.html', {
        'main_video': main_video,
        'page_obj': page_obj
    })