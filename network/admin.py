from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


# Register your models here.
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'date_joined']
    search_fields = ['username', 'email']


admin.site.register(User, UserAdmin)
