from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from .models import Employee
from .forms import EmployeeCreationForm  # Changed this line
from hr.models import Attendance
from .forms import EmployeeCreationForm, EmployeeChangeForm



class EmployeeLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.type in ['ADMIN', 'HR']:
            messages.success(self.request, f'Welcome back, {user.get_full_name()}!')
        else:
            messages.success(self.request, f'Welcome back, {user.get_full_name()}!')
        return reverse_lazy('accounts:dashboard')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password!')
        return super().form_invalid(form)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context.update({
            'user': user,
            'vacation_balance': user.vacation_balance,
        })

        # Add attendance data for employees
        if user.type not in ['ADMIN', 'HR']:
            context['today_attendance'] = Attendance.objects.filter(
                employee=user,
                date=timezone.now().date()
            ).first()
        
        # Add admin-specific context
        if user.type in ['ADMIN', 'HR']:
            context.update({
                'total_employees': Employee.objects.count(),
                'pending_requests': Employee.objects.filter(type='EMPLOYEE').count(),
            })
            
        return context

class EmployeeProfileView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'accounts/profile.html'
    context_object_name = 'employee'
    
    def get_object(self):
        return self.request.user
    

class EmployeeDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Employee
    template_name = 'accounts/employee_detail.html'
    context_object_name = 'employee'

    def test_func(self):
        return self.request.user.type in ['ADMIN', 'HR']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.get_object()
        context['vacation_requests'] = employee.vacation_requests.all()[:5]  # Last 5 requests
        context['attendance_records'] = employee.attendances.all()[:5]  # Last 5 attendance records
        return context

    


class EmployeeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Employee
    form_class = EmployeeCreationForm
    template_name = 'accounts/employee_form.html'
    success_url = reverse_lazy('hr:admin-vacation-list')

    def test_func(self):
        return self.request.user.type in ['ADMIN', 'HR']

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Employee "{form.instance.get_full_name()}" created successfully!')
        return response
    

class EmployeeListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Employee
    template_name = 'accounts/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10
    
    def test_func(self):
        return self.request.user.type in ['ADMIN', 'HR']
    
    def get_queryset(self):
        return Employee.objects.all().order_by('-date_joined')
    

class EmployeeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Employee
    form_class = EmployeeChangeForm
    template_name = 'accounts/employee_edit.html'
    success_url = reverse_lazy('accounts:employee-list')

    def test_func(self):
        return self.request.user.type in ['ADMIN', 'HR']

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Employee "{self.object.get_full_name()}" updated successfully!')
        return response

