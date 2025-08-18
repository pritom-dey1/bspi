from django.contrib import admin
from .models import Announcement, ContactMessage, Event, EventMomentImage, CustomUser, Person, LeaderboardMember, LearningMaterial, HelpPost, Comment
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm
# --- existing admin classes ---

@admin.register(LearningMaterial)
class LearningMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'wing')
    search_fields = ('title',)
    list_filter = ('wing',)

@admin.register(LeaderboardMember)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'project_name')

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'position')
    list_filter = ('role',)
    search_fields = ('name', 'position')

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'question', 'answer')

admin.site.register(Announcement, AnnouncementAdmin)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'message')


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser

    list_display = ('username', 'email', 'is_leader', 'is_staff')
    list_filter = ('session', 'department', 'wing', 'is_leader', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('session', 'department', 'wing', 'is_leader', 'profile_pic')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'session', 'department', 'wing', 'is_leader', 'profile_pic')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)

class EventMomentImageInline(admin.TabularInline):
    model = EventMomentImage
    extra = 1 

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventMomentImageInline]
    list_display = ('title', 'created_at')
    search_fields = ('title',)

# -------- Add HelpPost Admin --------

@admin.register(HelpPost)
class HelpPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    search_fields = ('title', 'content', 'user__username')
    list_filter = ('created_at',)

# -------- Add Comment Admin --------

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'content', 'created_at')
    search_fields = ('content', 'user__username', 'post__title')
    list_filter = ('created_at',)
