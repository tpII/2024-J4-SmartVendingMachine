from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Define the fields to display in the admin list view
    list_display = ('username', 'email', 'registration_method', 'is_staff', 'is_active')
    list_filter = ('registration_method', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

    # Define the fields to display in the admin detail view
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'registration_method')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Define the fields to display in the add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'registration_method', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

# Register the custom user admin with Django's admin
admin.site.register(User, CustomUserAdmin)
