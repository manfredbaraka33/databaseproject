from django.db import models
from django.db import models
from django.utils import timezone



class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField()
    address = models.TextField()
    password = models.CharField(max_length=128,default='xxxxxx') 
    image = models.ImageField(default="default.jpg",upload_to="pics") 


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        indexes = [
            models.Index(fields=['last_name']),
            models.Index(fields=['email']),
        ]

class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    specialization = models.CharField(max_length=100)
    available_from = models.TimeField()
    available_to = models.TimeField()
    password = models.CharField(max_length=128,default='xxxxxx') 
    image = models.ImageField(default="default.jpg",upload_to="pics") 

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} - {self.specialization}"
    
    
    class Meta:
        indexes = [
            models.Index(fields=['last_name']),
            models.Index(fields=['email']),
        ]

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='scheduled'
    )
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment with {self.doctor} on {self.appointment_date} at {self.appointment_time}"

    class Meta:
        unique_together = ('doctor', 'appointment_date', 'appointment_time')
        indexes = [
            models.Index(fields=['appointment_date', 'appointment_time']),
            models.Index(fields=['patient', 'appointment_date']),
        ]

