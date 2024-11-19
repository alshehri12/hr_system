from django.shortcuts import render

# Create your views here.
# organization/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Department
from .forms import DepartmentForm

class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'organization/department_list.html'
    context_object_name = 'departments'

class DepartmentDetailView(LoginRequiredMixin, DetailView):
    model = Department
    template_name = 'organization/department_detail.html'
    context_object_name = 'department'

class DepartmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'organization/department_form.html'
    success_url = reverse_lazy('organization:department-list')
    
    def test_func(self):
        return self.request.user.type in ['ADMIN', 'HR']

class DepartmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'organization/department_form.html'
    success_url = reverse_lazy('organization:department-list')
    
    def test_func(self):
        return self.request.user.type in ['ADMIN', 'HR']