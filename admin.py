from django.contrib import admin
from .models import Doctor,Patient,Appointment
from .forms import DoctorAdminForm

class DoctorAdmin(admin.ModelAdmin):
    form = DoctorAdminForm

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient)
admin.site.register(Appointment)
