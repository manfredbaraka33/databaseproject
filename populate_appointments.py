import random
from django.utils import timezone
from datetime import timedelta
from django.core.management.base import BaseCommand
from faker import Faker
from appointment.models import Appointment, Patient, Doctor  # Adjust the import based on your app name

class Command(BaseCommand):
    help = 'Populate the Appointment table with 120 entries'

    def handle(self, *args, **kwargs):
        faker = Faker()

        # Get all patients and doctors
        patients = list(Patient.objects.all())
        doctors = list(Doctor.objects.all())

        if not patients or not doctors:
            self.stdout.write(self.style.ERROR('No patients or doctors available to create appointments.'))
            return

        # Generate unique appointment times to avoid clashes
        appointments = set()

        for _ in range(120):
            patient = random.choice(patients)
            doctor = random.choice(doctors)

            # Ensure unique appointment time for the same doctor
            while True:
                appointment_date = faker.date_between(start_date='-1y', end_date='+1y')
                appointment_time = faker.time_object()
                appointment_key = (doctor, appointment_date, appointment_time)
                if appointment_key not in appointments:
                    appointments.add(appointment_key)
                    break

            status = random.choice(['scheduled', 'completed', 'cancelled'])
            notes = faker.text(max_nb_chars=200)

            Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status=status,
                notes=notes
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the Appointment table with 120 entries'))
