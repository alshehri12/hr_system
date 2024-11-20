# hr/models.py
from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import Employee
from django.utils import timezone
from datetime import datetime, time, timedelta
from django.utils.timezone import localtime

class VacationRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        CANCELED = 'CANCELED', 'Canceled'

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='vacation_requests'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    approved_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_vacations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.employee} - {self.start_date} to {self.end_date}"

    def clean(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError("End date must be after start date")
            if self.start_date < timezone.now().date():
                raise ValidationError("Start date cannot be in the past")

    def get_duration(self):
        return (self.end_date - self.start_date).days + 1

class Attendance(models.Model):
    employee = models.ForeignKey('accounts.Employee', on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    is_late = models.BooleanField(default=False)
    is_early_leave = models.BooleanField(default=False)

    OFFICE_START_TIME = time(7, 30)  # 7:30 AM
    LATE_THRESHOLD = time(8, 45)     # 8:45 AM
    WORK_HOURS = 8

    class Meta:
        ordering = ['-date']
        unique_together = ['employee', 'date']

    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.date}"

    def save(self, *args, **kwargs):
        if self.check_in:
            local_check_in = localtime(self.check_in)
            check_in_time = local_check_in.time()
            self.is_late = check_in_time > self.LATE_THRESHOLD

        if self.check_in and self.check_out:
            local_check_out = localtime(self.check_out)
            duration = local_check_out - localtime(self.check_in)
            hours_worked = duration.total_seconds() / 3600
            self.is_early_leave = hours_worked < self.WORK_HOURS

        super().save(*args, **kwargs)

    def get_check_in_time(self):
        if self.check_in:
            return localtime(self.check_in).strftime('%I:%M %p')
        return None

    def get_check_out_time(self):
        if self.check_out:
            return localtime(self.check_out).strftime('%I:%M %p')
        return None

    def get_duration(self):
        if self.check_in and self.check_out:
            duration = localtime(self.check_out) - localtime(self.check_in)
            hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60
            return f"{hours:02d}:{minutes:02d}"
        return None

    def get_status(self):
        if self.check_in and self.check_out:
            if self.is_late and self.is_early_leave:
                return 'Late & Early Leave'
            elif self.is_late:
                return 'Late'
            elif self.is_early_leave:
                return 'Early Leave'
            return 'Complete'
        elif self.check_in:
            if self.is_late:
                return 'Late - Working'
            return 'Working'
        return 'Absent'

    def get_required_hours(self):
        if self.check_in:
            local_check_in = localtime(self.check_in)
            expected_checkout = local_check_in + timedelta(hours=self.WORK_HOURS)
            return expected_checkout.strftime('%I:%M %p')
        return None
    

    def get_check_in_time(self):
        if self.check_in:
            return localtime(self.check_in).strftime('%I:%M %p')
        return None

    def get_check_out_time(self):
        if self.check_out:
            return localtime(self.check_out).strftime('%I:%M %p')
        return None

    

