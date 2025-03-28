from django.core.management.base import BaseCommand
from doctors.models import Doctor
import requests
from bs4 import BeautifulSoup

class Command(BaseCommand):
    help = 'Import doctors data'

    def handle(self, *args, **options):
        self.stdout.write('Starting import...')
        
        url = 'https://www.doctorsfinder.in/doctors/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        cards = soup.find_all('div', class_='card')
        
        for card in cards:
            try:
                name = card.find('h4', class_='card-title')
                if name:
                    name = name.text.strip()
                    doctor = Doctor.objects.create(
                        name=name,
                        specialization='General Physician'
                    )
                    self.stdout.write(f'Created doctor: {name}')
            except Exception as e:
                self.stdout.write(f'Error: {str(e)}')
        
        self.stdout.write('Import completed!') 