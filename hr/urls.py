# hr/urls.py
from django.urls import path
from . import views

app_name = 'hr'

urlpatterns = [
    # Employee URLs
    path('vacation/', views.EmployeeVacationListView.as_view(), name='employee-vacation-list'),
    path('vacation/request/', views.EmployeeVacationRequestView.as_view(), name='employee-vacation-create'),
    path('attendance/list/', views.EmployeeAttendanceListView.as_view(), name='employee-attendance-list'),
    path('attendance/check-in-out/', views.EmployeeAttendanceCheckView.as_view(), name='employee-attendance-check'),
    
    # Admin URLs
    path('admin/vacations/', views.AdminVacationListView.as_view(), name='admin-vacation-list'),
    path('admin/vacations/<int:pk>/approve/', views.AdminVacationApproveView.as_view(), name='admin-vacation-approve'),
    path('admin/vacations/<int:pk>/reject/', views.AdminVacationRejectView.as_view(), name='admin-vacation-reject'),
    path('admin/attendance/', views.AdminAttendanceListView.as_view(), name='admin-attendance-list'),
]