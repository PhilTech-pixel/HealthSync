from django.contrib import admin

import DataExchange
from DataExchange.models import UserProfile,PatientProfile,DoctorProfile,Hospital,AdminProfile,MedicalRecord,DataExchangeLog

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
admin.site.register(Hospital)
admin.site.register(AdminProfile)
admin.site.register(MedicalRecord)
admin.site.register(DataExchangeLog)