from django.core.management.base import BaseCommand
from doctors.models import Doctor, Organ

class Command(BaseCommand):
    help = 'Add Dr. Anchal Singh to the database'

    def handle(self, *args, **options):
        # Get the mental health specialization
        mental_health = Organ.objects.get(id=11)
        
        # Create Dr. Anchal Singh
        doctor = Doctor.objects.create(
            name='Anchal Singh',
            specialization=mental_health,
            clinic_address='123 Medical Center, New Delhi, India',
            experience=8,
            description='Dr. Anchal Singh is a highly experienced psychiatrist specializing in mental health disorders. She has extensive experience in treating anxiety, depression, and other mental health conditions. Dr. Singh is known for her compassionate approach and commitment to patient well-being.',
            photo='doctors/doctor_placeholder.jpg'  # You'll need to add an actual photo
        )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully added Dr. {doctor.name} to the database')) 