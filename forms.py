from django import forms
from django.contrib.auth.hashers import make_password
from .models import Doctor

class DoctorAdminForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return make_password(password)
