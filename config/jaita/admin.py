from django.contrib import admin
from .models import CustomUser, Patient, Doctor, Nurse, Appointment, MedicalRecord, Vitals

admin.site.register(CustomUser)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Appointment)
admin.site.register(MedicalRecord)
admin.site.register(Vitals)
