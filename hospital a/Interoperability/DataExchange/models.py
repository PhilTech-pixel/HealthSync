from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('Doctor', 'Doctor'),
        ('Patient', 'Patient'),
        ('Admin', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    contact_info = models.CharField(max_length=50, unique=True, null=True)
    is_approved = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username} - {self.role}"


class DoctorProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=255)
    license_number = models.CharField(max_length=50, unique=True)
    assigned_hospital = models.CharField(max_length=255)

    def __str__(self):
        return f"Dr. {self.user_profile.user.username} - {self.specialization}"

class PatientProfile(models.Model):
    patient_id = models.CharField(max_length=10, primary_key=True, editable=False, unique=True)
    user_profile = models.OneToOneField("UserProfile", on_delete=models.CASCADE)
    gender = models.CharField(
    max_length=10,
    choices=[("male", "Male"), ("female", "Female"), ("other", "Other")]
    )
    date_of_birth = models.DateField()
    blood_type = models.CharField(
    max_length=5,
    choices=[("A+", "A+"), ("A-", "A-"), ("B+", "B+"), ("B-", "B-"), ("AB+", "AB+"), ("AB-", "AB-"), ("O+", "O+"), ("O-", "O-")]
    )
    national_id = models.CharField(max_length=255)
    body_mass_index = models.FloatField()

    def save(self, *args, **kwargs):
        if not self.patient_id:  # Only set ID if it's not already assigned
            last_patient = PatientProfile.objects.order_by('-patient_id').first()
            if last_patient:
                last_number = int(last_patient.patient_id[1:])  # Extract number part
                new_number = last_number + 1
            else:
                new_number = 1  # Start at A1 if no patients exist
            self.patient_id = f"B{new_number}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient_id} - {self.user_profile.user.username}"


class Hospital(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class AdminProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    assigned_hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_profile.user.username} - @: {self.assigned_hospital}"


class MedicalRecord(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    medical_condition = models.TextField()
    date_of_admission = models.DateField()
    date_of_discharge = models.DateField()
    insurance_provider = models.CharField(max_length=255)
    admission_type = models.CharField(max_length=255)
    test_results = models.TextField()
    medication = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.patient.user_profile.user.username} - @: {self.hospital}"


class DataExchangeLog(models.Model):
    sender_hospital = models.ForeignKey(Hospital, related_name="sender", on_delete=models.CASCADE)
    receiver_hospital = models.ForeignKey(Hospital, related_name="receiver", on_delete=models.CASCADE)
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender_hospital.name} - to: {self.receiver_hospital.name}"

