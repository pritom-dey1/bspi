from django.contrib import admin
from .models import Announcement
from .models import ContactMessage
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

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
        'semester', 'department', 'wing',
        'is_email_verified', 'is_leader', 'last_login', 'is_staff'
    )

    # Add filters for easier filtering in admin sidebar
    list_filter = (
        'semester', 'department', 'wing', 'is_email_verified', 'is_leader', 'is_staff'
    )

    # Fieldsets to customize the user edit form in admin
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': (
                'semester', 'department', 'wing',
                'is_email_verified', 'verification_code',
                'is_leader',  # ✅ Add this line
            )
        }),
    )

    # Fields to show in the "Add User" form
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': (
                'semester', 'department', 'wing',
                'is_leader',  # ✅ Add this line
            )
        }),
    )
admin.site.register(CustomUser, CustomUserAdmin)
