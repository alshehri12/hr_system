# hr/forms.py
from django import forms
from .models import VacationRequest
from django.utils import timezone  # Add this import

class VacationRequestForm(forms.ModelForm):
    class Meta:
        model = VacationRequest
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("End date must be after start date.")
            if start_date < timezone.now().date():
                raise forms.ValidationError("Start date cannot be in the past.")
        
        return cleaned_data