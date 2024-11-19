# hr/models.py
from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import Employee
from django.utils import timezone

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
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    date = models.DateField(default=timezone.now)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    is_present = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['employee', 'date']
        
    def __str__(self):
        return f"{self.employee} - {self.date}"

    def clean(self):
        if self.check_out and self.check_in:
            if self.check_out < self.check_in:
                raise ValidationError("Check-out time must be after check-in time")

    def get_duration(self):
        if self.check_in and self.check_out:
            return self.check_out - self.check_in
        return None
    
    def get_duration(self):
        if self.check_in and self.check_out:
            duration = self.check_out - self.check_in
            hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60
            return f"{hours:02d}:{minutes:02d}"
        return None
