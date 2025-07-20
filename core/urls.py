from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('learning/', views.learning_page, name='learning'),
    path('go-to-learning/', views.redirect_learning, name='go_to_learning'),


    # ✅ Login/Logout routes
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # ✅ Custom system
    path('redirect/', views.post_login_redirect, name='post_login_redirect'),
    path('leader-dashboard/', views.leader_dashboard, name='leader_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('register/', views.register, name='register'),
    path('verify/', views.verify, name='verify'),
    path('announcements/', views.announcement_page, name='announcements'),
]
