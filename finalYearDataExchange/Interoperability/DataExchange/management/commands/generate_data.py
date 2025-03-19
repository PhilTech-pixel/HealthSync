from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker
from DataExchange.models import UserProfile, DoctorProfile, PatientProfile, Hospital, MedicalRecord


class Command(BaseCommand):
    help = 'Generate random medical record data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create hospitals
        hospitals = []
        for _ in range(5):  # Create 5 hospitals
            hospital = Hospital.objects.create(
                name=fake.company(),
                location=fake.city(),
                contact_info=fake.phone_number()
            )
            hospitals.append(hospital)

        # Create users and their profiles
        user_profiles = []
        for _ in range(10):  # Create 10 users
            username = fake.user_name()
            email = fake.email()

            user_profile = UserProfile.objects.create(
                user=User.objects.create_user(username=username, email=email, password='password123'),
                # Create User for each profile
                role=fake.random_choices(['Doctor', 'Patient', 'Admin']),
                contact_info=fake.phone_number(),
                is_approved=fake.boolean()
            )
            user_profiles.append(user_profile)

        # Create DoctorProfiles
        doctors = []
        for user_profile in user_profiles:
            if user_profile.role == 'Doctor':
                doctor = DoctorProfile.objects.create(
                    user_profile=user_profile,
                    specialization=fake.job(),
                    license_number=fake.unique.bothify(text='??####'),  # Generate unique license number
                    assigned_hospital=fake.random_choices([hospital.name for hospital in hospitals])
                )
                doctors.append(doctor)

        # Create PatientProfiles
        patients = []
        for user_profile in user_profiles:
            if user_profile.role == 'Patient':
                patient = PatientProfile.objects.create(
                    user_profile=user_profile,
                    date_of_birth=fake.date_of_birth(minimum_age=0, maximum_age=100),
                    national_id=fake.unique.uuid4()
                )
                patients.append(patient)

        # Create MedicalRecords
        medical_records = []
        for _ in range(50):  # Create 50 medical records
            medical_record = MedicalRecord.objects.create(
                patient=fake.random_choices(patients),
                doctor=fake.random_choices(doctors),
                diagnosis=fake.sentence(nb_words=6),
                treatment=fake.sentence(nb_words=10),
                hospital=fake.random_choice(hospitals)
            )
            medical_records.append(medical_record)

        self.stdout.write(self.style.SUCCESS('Successfully generated fake data!'))
