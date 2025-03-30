from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Organ, Doctor

# Common specialties with their icons - moved outside functions
specialties = [
    {'name': 'Cardiology', 'icon': 'fa-heartbeat'},
    {'name': 'Neurology', 'icon': 'fa-brain', 'query': 'neurology'},
    {'name': 'Psychiatry', 'icon': 'fa-user-md', 'query': 'psychiatry'},
    {'name': 'Oncology', 'icon': 'fa-lungs', 'query': 'oncology'},
    {'name': 'Dermatology', 'icon': 'fa-allergies', 'query': 'dermatology'},
    {'name': 'Plastic Surgery', 'icon': 'fa-bone', 'query': 'plastic surgery'},
    {'name': 'Orthopaedics', 'icon': 'fa-walking', 'query': 'orthopaedics'},
    {'name': 'Pediatrics', 'icon': 'fa-baby', 'query': 'pediatrics'},
    {'name': 'General Physician', 'icon': 'fa-stethoscope', 'query': 'general physician'},
    {'name': 'Pathologist', 'icon': 'fa-microscope', 'query': 'pathologist'},
    {'name': 'Dentist', 'icon': 'fa-tooth', 'query': 'dentist'},
    {'name': 'Allergist', 'icon': 'fa-virus-slash', 'query': 'allergist'}
]

def home(request):
    # Get organs from the database
    organs = Organ.objects.all()
    
    return render(request, 'doctors/home.html', {
        'organs': organs,
        'specialties': specialties
    })

def doctor_list(request, organ_id):
    organ = get_object_or_404(Organ, id=organ_id)
    # Get all doctors for specific organ first
    doctors = Doctor.objects.filter(specialization=organ)
    
    # Filter by experience if specified
    experience = request.GET.get('experience')
    if experience:
        try:
            if experience == '1+ years':
                doctors = doctors.filter(experience__gte=1)
            elif experience == '5+ years':
                doctors = doctors.filter(experience__gte=5)
            elif experience == '10+ years':
                doctors = doctors.filter(experience__gte=10)
            elif experience == '15+ years':
                doctors = doctors.filter(experience__gte=15)
        except Exception as e:
            # Log the error and continue without experience filter
            print(f"Error applying experience filter: {e}")
    
    # Search by location if specified
    location = request.GET.get('location')
    if location:
        # Split location into words and search for each word
        location_words = location.split()
        location_query = Q()
        for word in location_words:
            location_query |= Q(clinic_address__icontains=word)
        doctors = doctors.filter(location_query)
    
    # Apply limit after all filters
    doctors = doctors[:10]
    
    return render(request, 'doctors/doctor_list.html', {
        'organ': organ,
        'doctors': doctors,
        'filters': {
            'experience': experience,
            'location': location,
        },
        'specialties': specialties
    })

def search_doctors(request):
    query = request.GET.get('query', '')
    specialization_id = request.GET.get('specialization', '')
    location = request.GET.get('location', '')
    
    doctors = Doctor.objects.all()
    
    if query:
        # Map specialties to their corresponding organs
        if query.lower() == 'cardiology':
            # Get the Heart organ
            heart_organ = Organ.objects.filter(name__iexact='Heart').first()
            if heart_organ:
                doctors = doctors.filter(specialization=heart_organ)
        elif query.lower() == 'psychiatry':
            # Get the mental health organ
            mental_health_organ = Organ.objects.filter(name__iexact='mental health').first()
            if mental_health_organ:
                doctors = doctors.filter(specialization=mental_health_organ)
        elif query.lower() == 'neurology':
            # Get the Brain organ
            brain_organ = Organ.objects.filter(name__iexact='Brain').first()
            if brain_organ:
                doctors = doctors.filter(specialization=brain_organ)
        else:
            doctors = doctors.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(clinic_address__icontains=query) |
                Q(specialization__name__icontains=query)
            )
    
    if specialization_id and specialization_id.isdigit():
        doctors = doctors.filter(specialization_id=specialization_id)
    
    if location:
        doctors = doctors.filter(clinic_address__icontains=location)
    
    # Limit search results to 10 doctors
    doctors = doctors[:10]
    
    organs = Organ.objects.all()
    
    return render(request, 'doctors/search_results.html', {
        'doctors': doctors,
        'organs': organs,
        'query': query,
        'specialization_id': specialization_id,
        'location': location,
        'specialties': specialties
    })

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('doctors:home')
        else:
            return render(request, 'doctors/signin.html', {
                'error_message': 'Invalid username or password.',
                'specialties': specialties
            })
    
    return render(request, 'doctors/signin.html', {
        'specialties': specialties
    })

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        terms = request.POST.get('terms')
        
        # Validate form data
        if not all([username, email, password1, password2, terms]):
            return render(request, 'doctors/signup.html', {
                'error_message': 'All fields are required.',
                'specialties': specialties
            })
        
        if password1 != password2:
            return render(request, 'doctors/signup.html', {
                'error_message': 'Passwords do not match.',
                'specialties': specialties
            })
        
        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'doctors/signup.html', {
                'error_message': 'Username already exists.',
                'specialties': specialties
            })
        
        if User.objects.filter(email=email).exists():
            return render(request, 'doctors/signup.html', {
                'error_message': 'Email already registered.',
                'specialties': specialties
            })
        
        try:
            # Validate password strength
            validate_password(password1)
            
            # Create new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            
            # Log the user in
            login(request, user)
            
            return redirect('doctors:home')
            
        except ValidationError as e:
            return render(request, 'doctors/signup.html', {
                'error_message': ' '.join(e.messages),
                'specialties': specialties
            })
        except Exception as e:
            return render(request, 'doctors/signup.html', {
                'error_message': 'An error occurred. Please try again.',
                'specialties': specialties
            })
    
    return render(request, 'doctors/signup.html', {
        'specialties': specialties
    })
