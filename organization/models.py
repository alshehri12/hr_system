# organization/models.py
from django.db import models
from accounts.models import Employee

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    manager = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        related_name='managed_department'
    )
    employees = models.ManyToManyField(
        Employee,
        related_name='departments',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_employee_count(self):
        return self.employees.count()