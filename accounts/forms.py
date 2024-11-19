# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Employee




class EmployeeCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = ('username', 'employee_id', 'email', 'first_name', 'last_name', 
                 'type', 'date_of_birth', 'phone_number', 'address', 'hire_date')

class EmployeeChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Employee
        fields = ('username', 'email', 'first_name', 'last_name', 'type',
                 'date_of_birth', 'phone_number', 'address', 'profile_picture')
        

# accounts/forms.py
class EmployeeCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 
                 'last_name', 'employee_id', 'type', 'phone_number', 
                 'date_of_birth', 'hire_date', 'vacation_balance']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }

