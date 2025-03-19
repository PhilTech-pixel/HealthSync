from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, LoginForm, RegisterForm
from django.db.models.signals import post_save
from django.dispatch import receiver


import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import MedicalRecord, DataExchangeLog
from .serializers import MedicalRecordSerializer

from .models import UserProfile, PatientProfile, DoctorProfile, MedicalRecord, DataExchangeLog, AdminProfile, Hospital


# Create your views here.
def rregister(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('login')

    context = {'registerform': form}
    messages.success(request, 'Registration Successful')
    return render(request, 'registerpage.html', context=context)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # Hash the password
            user.save()

            # Create UserProfile with selected role
            role = form.cleaned_data["role"]
            UserProfile.objects.create(user=user, role=role)

            messages.success(request, "Registration successful. You can now log in.")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def my_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Get the user role from UserProfile
            try:
                role = user.userprofile.role
                if role == "doctor":
                    return redirect("doctor_dashboard")  # Replace with your actual URL name
                elif role == "patient":
                    return redirect("patient_dashboard")  # Replace with your actual URL name
            except UserProfile.DoesNotExist:
                messages.error(request, "User profile not found.")
                return redirect("login")
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, "login.html")

def user_logout(request):
    auth.logout(request)
    messages.success(request, 'Logout Successful')
    return redirect("/")

def home(request):
    return render(request,'login.html')

def index(request):
    return render(request,'index.html')

def d_register(request):
    return render(request,'d_register.html')
def p_register(request):
    return render(request,'p_register.html')

def doctor_register(request):
    if request.method == "POST":
        username = request.POST["full_name"]
        email = request.POST["email"]
        license_number = request.POST["license_number"]
        contact_info = request.POST["contact_info"]
        specialization = request.POST["specialization"]
        assigned_hospital = request.POST["assigned_hospital"]
        password = request.POST["password"]

        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()

         # Create UserProfile with role "doctor"
        user_profile = UserProfile.objects.create(user=user, contact_info=contact_info, role="doctor")
         # Create DoctorProfile with extra data
        DoctorProfile.objects.create(

            user_profile=user_profile,
            specialization=specialization,
            license_number=license_number,
            assigned_hospital=assigned_hospital,

        )

        messages.success(request, "Doctor registered successfully. You can now log in.")
        return redirect("login")
    else:
       return render(request, "d_register.html")

def patient_register(request):
    if request.method == "POST":
        username = request.POST["full_name"]
        email = request.POST["email"]
        national_id = request.POST["national_id"]
        contact_info = request.POST["contact_info"]
        date_of_birth = request.POST["date_of_birth"]
        password = request.POST["password"]

        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()

         # Create UserProfile with role "doctor"
        user_profile = UserProfile.objects.create(user=user, contact_info=contact_info, role="patient")
         # Create DoctorProfile with extra data
        PatientProfile.objects.create(

            user_profile=user_profile,
            national_id=national_id,
            date_of_birth=date_of_birth,


        )

        messages.success(request, "Patient registered successfully. You can now log in.")
        return redirect("login")
    else:
       return render(request, "d_register.html")



def custom_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.is_approved:
                if user_profile.role == "Doctor":
                    login(request, user)
                    return redirect("/doctor/dashboard")  # Change to appropriate dashboard
                elif user_profile.role == "Patient":
                    login(request, user)
                    return redirect("/patient/dashboard")
                elif user_profile.role == "Admin":
                    login(request, user)
                    return redirect("/administrator/dashboard")
            else:
                messages.error(request, "Your account is pending approval.")
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, "login.html")


def doctor_dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'doctor_dashboard.html', {'user_profile': user_profile})
def patient_dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'patient_dashboard.html', {'user_profile': user_profile})
def admin_dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'admin_dashboard.html', {'user_profile': user_profile})

def medical_records(request):
    user_profile = UserProfile.objects.get(user=request.user)
    records = MedicalRecord.objects.filter(doctor__user_profile=user_profile)
    return render(request, 'medical_records.html', {'records': records, 'user_profile': user_profile})

def access_medical_records(request):
    user_profile = UserProfile.objects.get(user=request.user)
    hospital = Hospital.objects.get(adminprofile__user_profile=user_profile)
    records = MedicalRecord.objects.filter(hospital=hospital)
    return render(request,'medical_display.html', {'records': records})


def data_transfer(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request,'data_transfer.html')

def data_exchange(request,id):
    user_profile = UserProfile.objects.get(user=request.user)
    medical_record = MedicalRecord.objects.get(id=id)
    sender_hospital = MedicalRecord.objects.get(hospital=medical_record.hospital)
    receiver_hospital = request.POST["receiver_hospital"]
    DataExchangeLog.objects.create(
        record=medical_record,
        sender_hospital=sender_hospital,
        receiver_hospital=receiver_hospital,
    )
    return redirect("/administrator/dashboard")


def search_patient(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')  # Get the patient_id from the form
        print(f"Searching for patient ID: {patient_id}")  # Debugging: Print the patient_id

        records = []
        patient_name = None  # Default to None in case it's not found locally

        try:
            # Try to fetch the patient profile locally
            patient_profile = PatientProfile.objects.get(patient_id=patient_id)
            print(f"Patient found: {patient_profile}")  # Debugging: Print the patient profile
            patient_name = patient_profile.user_profile.user.username

            # Fetch all medical records for the patient from the local database
            local_records = MedicalRecord.objects.filter(patient=patient_profile)
            print(f"Local records found: {local_records.count()}")  # Debugging: Print the number of local records
            
            for record in local_records:
                records.append({
                    'id': record.id,
                    'patient': patient_name,
                    'doctor': record.doctor.user_profile.user.username,
                    'diagnosis': record.diagnosis,
                    'treatment': record.treatment,
                    'created_at': record.created_at,
                    'source': 'Local Database',
                })

        except PatientProfile.DoesNotExist:
            # If the patient does not exist locally, query Hospital B before returning an error
            print("Patient not found locally. Querying Hospital B's API.")  
            api_records = fetch_records_from_hospital_a(patient_id)

            if api_records:
                print(f"Records fetched from Hospital B: {api_records}")  # Debugging: Print the API records
                patient_name = api_records[0]['patient']  # Get the patient name from the API response
                
                for api_record in api_records:
                    records.append({
                        'id': api_record['id'],
                        'patient': patient_name,
                        'doctor': api_record['doctor'],
                        'diagnosis': api_record['diagnosis'],
                        'treatment': api_record['treatment'],
                        'created_at': api_record['created_at'],
                        'source': 'Hospital A API',
                    })
            else:
                print("No records found in Hospital B.")  
                return render(request, 'search_patient.html', {'error': 'No records found for this patient in local database or Hospital A'})

        # Render the records in the template
        return render(request, 'search_patient.html', {'records': records, 'patient_name': patient_name})

    else:
        # Render the search form for GET requests
        return render(request, 'search_patient.html')





def fetch_records_from_hospital_a(patient_id):
    # Define the Hospital B API URL
    hospital_a_api_url = f"http://localhost:8000/api/get_patient_record/{patient_id}/"
    print(f"Querying Hospital B API: {hospital_a_api_url}")  # Debugging: Print the API URL
    
    try:
        # Make a GET request to the Hospital B API
        response = requests.get(hospital_a_api_url)
        print(f"Hospital B API response status code: {response.status_code}")  # Debugging: Print the status code
        print(f"Hospital B API response content: {response.content}")  # Debugging: Print the response content
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response JSON
            api_records = response.json()
            print(f"Records fetched from Hospital B: {api_records}")  # Debugging: Print the API records
            return api_records
        else:
            # Handle API errors (e.g., 404 Not Found, 500 Server Error)
            print(f"Hospital B API returned status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        # Handle connection errors (e.g., network issues)
        print(f"Error querying Hospital B API: {e}")
        return None




@api_view(['GET'])
@permission_classes([AllowAny]) # Secure access
def get_patient_record(request, patient_id):
    try:
        api_records = MedicalRecord.objects.filter(patient__patient_id=patient_id)
        serializer = MedicalRecordSerializer(api_records, many=True)
        return Response(serializer.data)
    except MedicalRecord.DoesNotExist:
        return Response({'error': 'No records found'}, status=404)
   






