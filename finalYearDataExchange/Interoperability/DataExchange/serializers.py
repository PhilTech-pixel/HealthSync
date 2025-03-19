from rest_framework import serializers
from .models import MedicalRecord



class MedicalRecordSerializer(serializers.ModelSerializer):
    # Use SerializerMethodField for patient and doctor to handle potential missing relationships
    patient = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()

    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'doctor', 'diagnosis', 'treatment', 'created_at']

    def get_patient(self, obj):
        # Safely get the patient's username
        if obj.patient and obj.patient.user_profile and obj.patient.user_profile.user:
            return obj.patient.user_profile.user.username
        return "Unknown Patient"

    def get_doctor(self, obj):
        # Safely get the doctor's username
        if obj.doctor and obj.doctor.user_profile and obj.doctor.user_profile.user:
            return obj.doctor.user_profile.user.username
        return "Unknown Doctor"