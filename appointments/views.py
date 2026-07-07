from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Appointment

# --- REST API imports ---
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import AppointmentSerializer

# ==================== WEB PAGES & CRUD ====================

def home_view(request):
    return render(request, 'index.html')

def doctors_view(request):
    return render(request, 'doctors.html')

def contact_view(request):
    return render(request, 'contact.html')

# View All & Add (Create) Appointment with Search Filter
def appointment_list_create(request):
    query = request.GET.get('search')
    if query:
        appointments = Appointment.objects.filter(patient_name__icontains=query) # Optional Search feature
    else:
        appointments = Appointment.objects.all()

    if request.method == "POST":
        patient_name = request.POST.get('patient_name')
        email = request.POST.get('email')
        doctor_name = request.POST.get('doctor_name')
        appointment_date = request.POST.get('appointment_date')
        symptoms = request.POST.get('symptoms')

        Appointment.objects.create(
            patient_name=patient_name,
            email=email,
            doctor_name=doctor_name,
            appointment_date=appointment_date,
            symptoms=symptoms
        )
        messages.success(request, "Appointment booked successfully!")
        return redirect('appointment_list')

    return render(request, 'appointments.html', {'appointments': appointments, 'query': query})

# Update Appointment
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        appointment.patient_name = request.POST.get('patient_name')
        appointment.email = request.POST.get('email')
        appointment.doctor_name = request.POST.get('doctor_name')
        appointment.appointment_date = request.POST.get('appointment_date')
        appointment.symptoms = request.POST.get('symptoms')
        appointment.save()
        messages.success(request, "Appointment updated successfully!")
        return redirect('appointment_list')
    return render(request, 'update_appointment.html', {'appointment': appointment})

# Delete Appointment
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    messages.success(request, "Appointment deleted successfully!")
    return redirect('appointment_list')


# ==================== REST API ENDPOINTS ====================

@api_view(['GET', 'POST'])
def api_appointments(request):
    if request.method == 'GET':
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def api_appointment_detail(request, pk):
    try:
        appointment = Appointment.objects.get(pk=pk)
    except Appointment.DoesNotExist:
        return Response({'error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = AppointmentSerializer(appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        appointment.delete()
        return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)