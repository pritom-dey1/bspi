from django.contrib import admin
from .models import Announcement
from .models import ContactMessage , Event, EventMomentImage
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Person
from .models import LeaderboardMember
from .models import LearningMaterial

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
    model = CustomUser

    # Fields to show in the list view of admin panel
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'session', 'department', 'wing',
        'is_email_verified', 'is_leader', 'last_login', 'is_staff'
    )

    # Add filters for easier filtering in admin sidebar
    list_filter = (
        'session', 'department', 'wing', 'is_email_verified', 'is_leader', 'is_staff'
    )

    # Customize the user edit form
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': (
                'session', 'department', 'wing',
                'is_email_verified', 'verification_code',
                'is_leader', 'profile_pic'  # 👈 Add profile_pic here
            )
        }),
    )

    # Customize the user creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': (
                'session', 'department', 'wing',
                'is_leader', 'profile_pic'  # 👈 Add profile_pic here
            )
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
