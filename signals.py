# appointment/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from appointment.models import Patient, Doctor, Appointment
from datawarehousex.management.commands.etl import Command as ETLCommand

# @receiver(post_save, sender=Patient)
# @receiver(post_save, sender=Doctor)
# @receiver(post_save, sender=Appointment)
# def run_etl(sender, instance, created, **kwargs):
#     if created:
#         # If a new instance is created, run the ETL process
#         etl_command = ETLCommand()
#         etl_command.handle()
