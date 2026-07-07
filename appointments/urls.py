from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('doctors/', views.doctors_view, name='doctors'),
    path('contact/', views.contact_view, name='contact'),
    path('appointments/', views.appointment_list_create, name='appointment_list'),
    path('appointments/update/<int:pk>/', views.appointment_update, name='appointment_update'),
    path('appointments/delete/<int:pk>/', views.appointment_delete, name='appointment_delete'),

    # API Endpoints
    path('api/appointments/', views.api_appointments, name='api_appointments'),
    path('api/appointments/<int:pk>/', views.api_appointment_detail, name='api_appointment_detail'),
]