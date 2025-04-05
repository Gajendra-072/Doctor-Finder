# Doctor Specialist Finder

A Django-based web application that helps users discover medical specialists for specific diseases. The platform provides a modern, user-friendly interface with dynamic content and real-time doctor availability.

## Features

- **Specialist Discovery**: Find doctors specialized in specific medical conditions
- **Dynamic UI**: Beautiful, responsive interface with rotating medical-themed background images
- **User Authentication**: Secure login and registration system
- **Doctor Profiles**: Detailed information about medical specialists
- **Appointment Booking**: Schedule appointments with preferred doctors
- **Admin Dashboard**: Comprehensive admin interface for managing doctors and appointments

## Technology Stack

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default)
- **UI Framework**: Bootstrap
- **Image API**: Unsplash API for dynamic background images

## Project Structure

```
doctor/
├── doctors/                 # Main application directory
│   ├── templates/          # HTML templates
│   │   ├── doctors/       # Doctor-specific templates
│   │   └── base.html      # Base template
│   ├── static/            # Static files (CSS, JS, images)
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   └── urls.py            # URL routing
├── manage.py              # Django management script
└── requirements.txt       # Project dependencies
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Gajendra-001/Doctor-Finder-.git
cd doctor
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Configuration

The application uses the following environment variables:
- `UNSPLASH_ACCESS_KEY`: API key for Unsplash image service
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode setting

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Background images provided by [Unsplash](https://unsplash.com)
- Icons and UI elements from Bootstrap
