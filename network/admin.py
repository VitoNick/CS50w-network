from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Post, User


# Register your models here.
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'date_joined']
    search_fields = ['username', 'email']


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'content_preview', 'created_at']
    list_filter = ['created_at', 'owner']
    search_fields = ['contents', 'owner__username']
    readonly_fields = ['created_at']
    
    def content_preview(self, obj):
        """Show first 50 characters of post content"""
        return obj.contents[:50] + '...' if len(obj.contents) > 50 else obj.contents
    content_preview.short_description = 'Content'


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)

