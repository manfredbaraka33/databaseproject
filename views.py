from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from .models import Patient,Doctor,Appointment
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.management import call_command

def index(request):
    return render(request,'appointment/index.html')


def intLog(request):
    return render(request,'appointment/intLog.html')


def login(request):  
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            patient = Patient.objects.get(email=email)
            if check_password(password, patient.password):
                request.session['patient_id'] = patient.id  
                messages.success(request, 'Login successful')
                return redirect('appointment:patientDb') 
               
            else:
                messages.error(request, 'Invalid password')
        except Patient.DoesNotExist:
            messages.error(request, 'Invalid email')
    
    return render(request,'appointment/login.html')



def login2(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            doctor = Doctor.objects.get(email=email)
            if check_password(password, doctor.password):
                request.session['doctor_id'] = doctor.id
                request.session.save() 
                messages.success(request, 'Login successful')
                return redirect('appointment:doctorDb') 
            else:
                messages.error(request, 'Invalid password')
        except Doctor.DoesNotExist:
            messages.error(request, 'Invalid email')
    
    return render(request, 'appointment/login2.html')



def register(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        db = request.POST.get('db')
        address = request.POST.get('address')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        image = request.FILES.get('image') 
        
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'appointment/register.html')

       
        if Patient.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'appointment/register.html')
        if Patient.objects.filter(phone_number=phone).exists():
            messages.error(request, 'Phone number already exists')
            return render(request, 'appointment/register.html')
        
     
        hashed_password = make_password(password)

        patient = Patient(
            first_name=fname,
            last_name=lname,
            email=email,
            phone_number=phone,
            date_of_birth=db,
            address=address,
            password=hashed_password,
            image=image
        )
        
        with transaction.atomic():
                call_command('etl')  
                
        patient.save()
            
        messages.success(request, 'Registration successful')
        return redirect('appointment:login') 
    return render(request,'appointment/register.html')

def patientDb(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        messages.error(request, 'You need to login first')
        return redirect('appointment:login2')
    patient = Patient.objects.get(id=patient_id)
    appointments = Appointment.objects.filter(patient=patient)
    listcancelled = Appointment.objects.filter(patient=patient,status='Cancelled')
    cancelled = Appointment.objects.filter(patient=patient,status='Cancelled').count()
    listscheduled = Appointment.objects.filter(patient=patient,status='scheduled')
    scheduled = Appointment.objects.filter(patient=patient,status='scheduled').count()
    listcompleted = Appointment.objects.filter(patient=patient,status='Completed')
    completed = Appointment.objects.filter(patient=patient,status='Completed').count()
    apCount=appointments.count()
    return render(request, 'appointment/patientDb.html', {'patient': patient,
                                                          'apCount':apCount,
                                                          'cancelled':cancelled,
                                                          'scheduled':scheduled,
                                                          'completed':completed,
                                                          'listcancelled':listcancelled,
                                                          'listscheduled':listscheduled,
                                                         'listcompleted':listcompleted,
                                                          })

def doctorDb(request):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        messages.error(request, 'You need to login first')
        return redirect('appointment:login2')

    doctor = Doctor.objects.get(id=doctor_id)
    appointments = Appointment.objects.filter(doctor=doctor)
    doctor_id = request.session.get('doctor_id')
    doctor = Doctor.objects.get(id=doctor_id)
    listcancelled = Appointment.objects.filter(doctor=doctor,status='Cancelled')
    cancelled = Appointment.objects.filter(doctor=doctor,status='Cancelled').count()
    listscheduled = Appointment.objects.filter(doctor=doctor,status='scheduled')
    scheduled = Appointment.objects.filter(doctor=doctor,status='scheduled').count()
    listcompleted = Appointment.objects.filter(doctor=doctor,status='Completed')
    completed = Appointment.objects.filter(doctor=doctor,status='Completed').count()
    apCount=appointments.count()
    return render(request,
                  'appointment/doctorDb.html', 
                  {'doctor': doctor,'apCount':apCount,
                   'cancelled':cancelled,
                    'scheduled':scheduled,
                    'completed':completed,
                    'listcancelled':listcancelled,
                    'listscheduled':listscheduled,
                    'listcompleted':listcompleted,
                    })

def makeAppointment(request):
    if request.method == 'POST':
        patient_id = request.session.get('patient_id')
        if not patient_id:
            messages.error(request, 'You need to be logged in to make an appointment.')
            return redirect('appointment:login')

        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        notes = request.POST.get('notes', '')

        try:
            patient = Patient.objects.get(id=patient_id)
            doctor = Doctor.objects.get(id=doctor_id)
            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                notes=notes
            )
            
            
            with transaction.atomic():
                call_command('etl')  


            
            messages.success(request, 'Appointment made successfully!')
            return redirect('appointment:patientDb')
        except Patient.DoesNotExist:
            messages.error(request, 'Invalid patient.')
        except Doctor.DoesNotExist:
            messages.error(request, 'Invalid doctor.')
        except Exception as e:
            messages.error(request, f'Error making appointment: {e}')
    patient_id = request.session.get('patient_id')
    patient = Patient.objects.get(id=patient_id)        
 
    doctors = Doctor.objects.all()
    return render(request, 'appointment/makeAppointment.html', {'doctors': doctors,'patient':patient})


def appointments(request):
    patient_id = request.session.get('patient_id')
    patient = Patient.objects.get(id=patient_id)
    appointments = Appointment.objects.filter(patient=patient)
    apCount=appointments.count()
    return render(request, 'appointment/appointments.html', {'patient': patient, 'appointments': appointments,'apCount':apCount})


def appointments2(request):
    doctor_id = request.session.get('doctor_id')
    doctor = Doctor.objects.get(id=doctor_id)
    appointments = Appointment.objects.filter(doctor=doctor)
    apCount=appointments.count()
    return render(request, 'appointment/appointments2.html', {'doctor': doctor, 'appointments': appointments,'apCount':apCount})



def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    doctors = Doctor.objects.all()
    
    if request.method == 'POST':
        appointment.appointment_date = request.POST.get('appointment_date')
        appointment.appointment_time = request.POST.get('appointment_time')
        doctor_id = request.POST.get('doctor')  # Fetch the doctor ID from the form
        doctor = get_object_or_404(Doctor, id=doctor_id)  # Fetch the Doctor instance by ID
        appointment.doctor = doctor
        appointment.notes = request.POST.get('notes')
        appointment.status = request.POST.get('status')
        
        with transaction.atomic():
                call_command('etl')  
        
        appointment.save()
        messages.success(request, 'Appointment updated successfully')
        return redirect('appointment:appointments') 
    
    patient_id = request.session.get('patient_id')
    patient = Patient.objects.get(id=patient_id) 


    return render(request, 'appointment/edit_appointment.html', {'doctors': doctors,'appointment': appointment,'patient':patient})


def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        appointment.status='Cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully')
        return redirect('appointment:appointments')  
    
    patient_id = request.session.get('patient_id')
    patient = Patient.objects.get(id=patient_id)
    
    return render(request, 'appointment/cancel_confirmation.html', {'appointment': appointment,'patient':patient})


def mark_complete(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        appointment.status='Completed'
        appointment.save()
        messages.success(request, 'Appointment marked completed successfully')
        return redirect('appointment:appointments2')  
    
    doctor_id = request.session.get('doctor_id')
    doctor = Doctor.objects.get(id=doctor_id)
    
    return render(request, 'appointment/mark_complete.html', {'appointment': appointment,'doctor':doctor})


def account(request):
    patient_id = request.session.get('patient_id')
    patient = Patient.objects.get(id=patient_id)
    return render(request, 'appointment/account.html', {'patient':patient})

def account2(request):
    doctor_id = request.session.get('doctor_id')
    doctor = Doctor.objects.get(id=doctor_id)
    return render(request, 'appointment/account2.html', {'doctor':doctor})
    