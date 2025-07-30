from django.urls import path
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/',views.about_page,name='about'),
    path('learning/', views.learning_page, name='learning'),
    path('go-to-learning/', views.redirect_learning, name='go_to_learning'),
    path('announcement/<int:id>/', views.announcement_detail, name='announcement_detail'),
    path('events/', views.event_list, name='event_list'),
    # ✅ Login/Logout routes
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('event/<int:id>/', views.event_detail, name='event_detail'),
    # ✅ Custom system
    path('leader/approve/<int:user_id>/', views.approve_member, name='approve_member'),
    path('redirect/', views.post_login_redirect, name='post_login_redirect'),
    path('leader-dashboard/', views.leader_dashboard, name='leader_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('register/', views.register, name='register'),
    path('verify/', views.verify, name='verify'),
    path('announcements/', views.announcement_page, name='announcements'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)