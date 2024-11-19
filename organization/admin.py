# organization/admin.py
from django.contrib import admin
from .models import Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'manager', 'get_employee_count', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code', 'manager__username')
    filter_horizontal = ('employees',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'code', 'description')
        }),
        ('Management', {
            'fields': ('manager', 'employees', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )