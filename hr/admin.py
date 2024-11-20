from django.contrib import admin

# Register your models here.
# hr/admin.py
from django.contrib import admin
from .models import VacationRequest, Attendance

@admin.register(VacationRequest)
class VacationRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('status', 'start_date', 'employee')
    search_fields = ('employee__username', 'employee__email', 'reason')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('employee', 'start_date', 'end_date', 'reason')
        }),
        ('Status', {
            'fields': ('status', 'approved_by', 'comments')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in', 'check_out', 'is_late', 'is_early_leave')
    list_filter = ('date', 'is_late', 'is_early_leave')
    search_fields = ('employee__first_name', 'employee__last_name', 'employee__employee_id')
    date_hierarchy = 'date'