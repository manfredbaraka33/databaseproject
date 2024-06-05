from django.urls import path

from . import views


app_name = "appointment"
urlpatterns = [
    
  path("", views.index, name="index"),
  path("intLogin", views.intLog, name="intLog"),
  path("login", views.login, name="login"),
  path("login2", views.login2, name="login2"),
  path("register", views.register, name="register"),
  path("patientDb", views.patientDb, name="patientDb"),
  path("account", views.account, name="account"),
  path("account2", views.account2, name="account2"),
  path("doctorDb", views.doctorDb, name="doctorDb"),
  path("makeAppointment", views.makeAppointment, name="makeAppointment"),
  path("Appointments", views.appointments, name="appointments"),
  path("Appointments2", views.appointments2, name="appointments2"),
  path('appointments/edit/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
  path('appointments/cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
  path('appointments/complete/<int:appointment_id>/', views.mark_complete, name='mark_complete'),

]