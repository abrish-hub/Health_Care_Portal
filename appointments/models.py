from django.db import models

class Appointment(models.Model):
    patient_name = models.CharField(max_length=100)
    email = models.EmailField()
    doctor_name = models.CharField(max_length=100)
    appointment_date = models.DateField()
    symptoms = models.TextField()

    def __str__(self):
        return f"{self.patient_name} - {self.doctor_name}"