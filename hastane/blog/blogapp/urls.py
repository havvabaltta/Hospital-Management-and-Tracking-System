from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', views.admin_page, name='admin'),  # Existing path for admin page
    path('doctor/', views.doctor_page, name='doctor'),
    path('patient/', views.patient_page, name='patient'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('doctor-login/', views.doctor_login, name='doctor_login'),
    path('patient-login/', views.patient_login, name='patient_login'),

    path('add_patient/', views.add_patient, name='add_patient'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('delete_patient/', views.delete_patient, name='delete_patient'),
    path('delete_doctor/', views.delete_doctor, name='delete_doctor'),
 
    path('update_patient/', views.update_patient, name='update_patient'),
    path('update_doctor/', views.update_doctor, name='update_doctor'),
    path('add_report/', views.add_report, name='add_report'),
    path('delete_report/', views.delete_report, name='delete_report'),
    path('update_report/', views.update_report, name='update_report'),
    path('update_appointment/', views.update_appointment, name='update_appointment'),

    #path('view_patients/', views.view_patients, name='view_patients'),
    #path('view_doctors/', views.view_doctors, name='view_doctors'),
    #path('admin/appointments/', views.view_all_appointments, name='view_all_appointments'),
    #path('api/reports/', views.viewReports, name='viewReports'),
  
    path('api/appointments/<int:pid>', views.patient_show_randevu, name='patient_show_randevu'),
    path('api/profil/<int:pid>', views.patient_profil, name='patient_profil'),
    path('api/randevu/<int:pid>', views.patient_add_randevu, name='patient_add_randevu'),
    path('api/deleteAppointment/<int:rid>/', views.patient_delete_randevu, name='deleteAppointment'),
    path('api/reports/', views.list_reports, name='list_reports'),
    path('api/patients/', views.list_patients, name='list_patients'),
    path('api/doctors/', views.list_doctors, name='list_doctors'),
    path('api/appointments/', views.list_appointments, name='list_appointments'),
    path('api/doctor/randevu/<int:did>', views.doctor_show_randevu, name='doctor_show_randevu'),
    path('api/doctor/patients/<int:did>/', views.doctor_got_patients, name='doctor_patients'),
    


    path('api/patient/<int:pid>/reports/', views.patient_show_reports, name='patient_reports'),
    path('api/doctor/<int:did>/reports/', views.doctor_show_reports, name='doctor_show_reports'),
    path('doctor/add_report/', views.doctor_add_report, name='doctor_add_report'),
]
