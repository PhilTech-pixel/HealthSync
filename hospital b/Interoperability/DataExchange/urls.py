from django.contrib import admin
from django.urls import path, include

from DataExchange import views
#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', views.home, name='login'),
    path("register/", views.register, name="register"),
    path("", views.index, name="index"),
    path("register/doctor/", views.d_register, name="doctorregistration"),
    path("doctorregister/", views.doctor_register, name="drregistration"),
    path("register/patient/",views.p_register, name="patientregistration"),
    path("patientregister/", views.patient_register, name="pregistration"),
    path("doctor/dashboard/", views.doctor_dashboard, name="doctor_dashboard"),
    path("patient/dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path("administrator/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("custom_login/", views.custom_login, name="custom_login"),
    path("logout/",views.user_logout, name="logout"),
    path("medicalrecords/", views.medical_records, name="medical_records"),
    path("medicaldisplay/", views.access_medical_records, name="access_medical_records"),
    path("administrator/datatransfer/", views.data_transfer, name="data_transfer"),
    path('api/get_patient_record/<str:patient_id>/', views.get_patient_record, name='get_patient_record'),
    path('api/fetch_records_from_hospital_a/<str:patient_id>/', views.fetch_records_from_hospital_a, name='fetch_records_from_hospital_a'),
    path('search_patient/', views.search_patient, name='search_patient'),

]