# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'employee_id', 'type')
    list_filter = ('type', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'employee_id', 'email')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'employee_id', 'type')
        }),
        ('Additional info', {
            'fields': ('date_of_birth', 'phone_number', 'address', 'hire_date', 'vacation_balance')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'employee_id', 
                      'first_name', 'last_name', 'type'),
        }),
    )

    ordering = ('username',)