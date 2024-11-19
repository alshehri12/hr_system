# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Employee(AbstractUser):
    class EmployeeType(models.TextChoices):
        ADMIN = 'ADMIN', _('Administrator')
        HR = 'HR', _('HR Manager')
        EMPLOYEE = 'EMPLOYEE', _('Employee')
        MANAGER = 'MANAGER', _('Manager')

    # Personal Information
    employee_id = models.CharField(max_length=10, unique=True, help_text="Unique employee ID")
    type = models.CharField(
        max_length=10, 
        choices=EmployeeType.choices,
        default=EmployeeType.EMPLOYEE
    )
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    
    # Employment Information
    hire_date = models.DateField(null=True, blank=True)
    vacation_balance = models.PositiveIntegerField(default=21)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        return f"{self.get_full_name()} ({self.employee_id})"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('accounts:employee-detail', kwargs={'pk': self.pk})