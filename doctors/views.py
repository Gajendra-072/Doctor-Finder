from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Organ, Doctor

# Common specialties with their icons - moved outside functions
specialties = [
    {'name': 'Cardiology', 'icon': 'fa-heartbeat'},
    {'name': 'Neurology', 'icon': 'fa-brain', 'query': 'neurology'},
    {'name': 'Psychiatry', 'icon': 'fa-user-md', 'query': 'psychiatry'},
    {'name': 'Oncology', 'icon': 'fa-lungs'},
    {'name': 'Dermatology', 'icon': 'fa-allergies'},
    {'name': 'Plastic Surgery', 'icon': 'fa-bone'},
    {'name': 'Orthopaedics', 'icon': 'fa-walking'},
    {'name': 'Pediatrics', 'icon': 'fa-baby'},
    {'name': 'General Physician', 'icon': 'fa-stethoscope'},
    {'name': 'Pathologist', 'icon': 'fa-microscope'},
    {'name': 'Dentist', 'icon': 'fa-tooth'},
    {'name': 'Allergist', 'icon': 'fa-virus-slash'}
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
    # Show all doctors for specific organ with a limit of 10
    doctors = Doctor.objects.filter(specialization=organ)[:10]
    
    # Filter by experience if specified
    experience = request.GET.get('experience')
    if experience:
        if experience == '1+ years':
            doctors = doctors.filter(experience__gte=1)
        elif experience == '5+ years':
            doctors = doctors.filter(experience__gte=5)
        elif experience == '10+ years':
            doctors = doctors.filter(experience__gte=10)
        elif experience == '15+ years':
            doctors = doctors.filter(experience__gte=15)
    
    # Search by location if specified
    location = request.GET.get('location')
    if location:
        doctors = doctors.filter(clinic_address__icontains=location)
    
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
