# hr/views.py
from django.views.generic import ListView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from .models import VacationRequest, Attendance
from .forms import VacationRequestForm
from .models import VacationRequest
from .models import Attendance

from django.views.generic import ListView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import VacationRequest
from accounts.models import Employee
from django.utils.timezone import localtime
from django.utils import timezone

# Employee Views

class EmployeeVacationRequestView(LoginRequiredMixin, CreateView):
    model = VacationRequest
    form_class = VacationRequestForm
    template_name = 'hr/employee/vacation_request_form.html'
    success_url = reverse_lazy('hr:employee-vacation-list')

    def form_valid(self, form):
        form.instance.employee = self.request.user
        form.instance.status = 'PENDING'
        messages.success(self.request, 'Vacation request submitted successfully!')
        return super().form_valid(form)

class EmployeeAttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'hr/employee/attendance_list.html'
    context_object_name = 'attendance_records'
    
    def get_queryset(self):
        return Attendance.objects.filter(
            employee=self.request.user
        ).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        context['today_attendance'] = Attendance.objects.filter(
            employee=self.request.user,
            date=today
        ).first()
        return context

class EmployeeAttendanceCheckView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        today = timezone.now().date()
        attendance, created = Attendance.objects.get_or_create(
            employee=request.user,
            date=today
        )
        
        action = request.POST.get('action')
        if action == 'check_in' and not attendance.check_in:
            attendance.check_in = timezone.now()
            attendance.save()
            messages.success(request, 'Successfully checked in!')
        elif action == 'check_out' and attendance.check_in and not attendance.check_out:
            attendance.check_out = timezone.now()
            attendance.save()
            messages.success(request, 'Successfully checked out!')
            
        return redirect('hr:employee-attendance-list')



# Admin Views
# hr/views.py
class AdminVacationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = VacationRequest
    template_name = 'hr/admin/vacation_list.html'
    context_object_name = 'vacation_requests'
    paginate_by = 10
    
    def test_func(self):
        return self.request.user.type in ['ADMIN', 'HR']
    
    def get_queryset(self):
        status = self.request.GET.get('status')
        queryset = VacationRequest.objects.all().order_by('-created_at')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'pending_count': VacationRequest.objects.filter(status='PENDING').count(),
            'approved_count': VacationRequest.objects.filter(status='APPROVED').count(),
            'rejected_count': VacationRequest.objects.filter(status='REJECTED').count(),
            'total_count': VacationRequest.objects.count(),
        })
        return context

class AdminVacationApproveView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.type in ['ADMIN', 'HR']
        
    def post(self, request, pk):
        vacation = get_object_or_404(VacationRequest, pk=pk)
        
        # Calculate vacation days
        days_requested = (vacation.end_date - vacation.start_date).days + 1
        
        # Check if employee has enough balance
        if vacation.employee.vacation_balance >= days_requested:
            vacation.status = 'APPROVED'
            vacation.approved_by = request.user
            vacation.save()
            
            # Deduct days from balance
            vacation.employee.vacation_balance -= days_requested
            vacation.employee.save()
            
            messages.success(request, 'Vacation request approved successfully!')
        else:
            messages.error(request, 'Insufficient vacation balance!')
        
        return redirect('hr:admin-vacation-list')


class AdminVacationRejectView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.type in ['ADMIN', 'HR']
        
    def post(self, request, pk):
        vacation = get_object_or_404(VacationRequest, pk=pk)
        vacation.status = 'REJECTED'
        vacation.comments = request.POST.get('comment')
        vacation.approved_by = request.user
        vacation.save()
        messages.success(request, 'Vacation request rejected')
        return redirect('hr:admin-vacation-list')
    

class AdminAttendanceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Attendance
    template_name = 'hr/admin/attendance_list.html'
    context_object_name = 'attendance_records'
    
    def test_func(self):
        return self.request.user.type in ['ADMIN', 'HR']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        context['employees'] = Employee.objects.all()
        return context

    def get_queryset(self):
        queryset = Attendance.objects.all()
        
        # Filter by date
        date = self.request.GET.get('date')
        if date:
            queryset = queryset.filter(date=date)
        else:
            queryset = queryset.filter(date=timezone.now().date())
            
        # Filter by employee
        employee_id = self.request.GET.get('employee')
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)
            
        return queryset.order_by('-date', 'employee__first_name')



class EmployeeVacationListView(LoginRequiredMixin, ListView):
    model = VacationRequest
    template_name = 'hr/employee/vacation_list.html'
    context_object_name = 'vacation_requests'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        return VacationRequest.objects.filter(
            employee=self.request.user
        ).order_by('-created_at')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        print(f"User: {self.request.user.username}")
        print(f"Vacation Requests: {self.get_queryset().count()}")
        return context
    

class EmployeeAttendanceView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        today = timezone.localtime().date()
        
        attendance, created = Attendance.objects.get_or_create(
            employee=request.user,
            date=today
        )
        
        if action == 'check_in' and not attendance.check_in:
            attendance.check_in = timezone.localtime()
            attendance.save()
            messages.success(request, 'Checked in successfully!')
        elif action == 'check_out' and attendance.check_in and not attendance.check_out:
            attendance.check_out = timezone.localtime()
            attendance.save()
            messages.success(request, 'Checked out successfully!')
        
        return redirect('hr:employee-attendance-list')


