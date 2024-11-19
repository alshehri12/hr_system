from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.EmployeeLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='accounts:login', http_method_names=['get', 'post']), name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('profile/', views.EmployeeProfileView.as_view(), name='profile'),
    path('employees/', views.EmployeeListView.as_view(), name='employee-list'),
    path('employee/add/', views.EmployeeCreateView.as_view(), name='employee-create'),
    path('employee/create/', views.EmployeeCreateView.as_view(), name='employee-create'),
    path('employees/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employees/<int:pk>/edit/', views.EmployeeUpdateView.as_view(), name='employee-edit'),

]