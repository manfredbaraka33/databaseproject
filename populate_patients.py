import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from faker import Faker
from appointment.models import Patient  # Adjust the import based on your app name

class Command(BaseCommand):
    help = 'Populate the Patient table with 120 entries'

    def handle(self, *args, **kwargs):
        faker = Faker()

        tanzanian_first_names = [
            'Amani', 'Baraka', 'Juma', 'Saidi', 'Mwanajuma', 'Hassan', 'Fatuma', 'Asha', 'Mwajuma', 'Abdul', 'Kassim', 'Salma', 'Ramadhani', 'Halima', 'Rehema', 'Shabani'
        ]

        tanzanian_last_names = [
            'Mwinyi', 'Ngoma', 'Mosha', 'Mabula', 'Mtui', 'Makamba', 'Nyerere', 'Magufuli', 'Mkapa', 'Kikwete', 'Mwakyusa', 'Mwalimu', 'Mwakalebela', 'Mwapachu', 'Mpangala'
        ]

        # Generate unique email and phone number
        def unique_email():
            return faker.unique.email()

        def unique_phone_number():
            return faker.unique.numerify(text='###########')  # Generates a 10-11 digit number

        for _ in range(120):
            first_name = random.choice(tanzanian_first_names)
            last_name = random.choice(tanzanian_last_names)
            email = unique_email()
            phone_number = unique_phone_number()
            date_of_birth = faker.date_of_birth(minimum_age=18, maximum_age=90)
            address = faker.address()
            image = "default.jpg"  # Assuming a default image

            Patient.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                date_of_birth=date_of_birth,
                address=address,
                image=image
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the Patient table with 120 entries'))
