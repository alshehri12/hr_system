# organization/forms.py
from django import forms
from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description', 'manager', 'employees', 'is_active']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show employees with manager type for manager field
        self.fields['manager'].queryset = self.fields['manager'].queryset.filter(
            type__in=['MANAGER', 'ADMIN']
        )