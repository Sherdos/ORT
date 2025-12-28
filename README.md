# ORT Django Web App

A fully functional Django web application built with Django 6.0 and Python 3.12.

## Features

- ✅ Django 6.0 Framework
- ✅ Modern responsive web interface
- ✅ URL routing and views
- ✅ Template inheritance with base template
- ✅ Multiple pages (Home, About)
- ✅ Admin interface ready
- ✅ SQLite database configured
- ✅ Ready for development and extension

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Sherdos/ORT.git
cd ORT
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run database migrations:
```bash
python manage.py migrate
```

## Running the Application

Start the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Project Structure

```
ORT/
├── manage.py              # Django management script
├── ort_project/          # Project configuration
│   ├── settings.py       # Project settings
│   ├── urls.py           # URL routing
│   └── wsgi.py           # WSGI configuration
├── main/                 # Main application
│   ├── views.py          # View functions
│   ├── urls.py           # App URL routing
│   ├── models.py         # Database models
│   └── templates/        # HTML templates
└── requirements.txt      # Python dependencies
```

## Available Pages

- **Home**: `http://127.0.0.1:8000/` - Main landing page
- **About**: `http://127.0.0.1:8000/about/` - About page
- **Admin**: `http://127.0.0.1:8000/admin/` - Django admin interface

## Creating an Admin User

To access the admin interface, create a superuser:
```bash
python manage.py createsuperuser
```

Follow the prompts to set up username, email, and password.

## Next Steps

You can extend this application by:
- Creating database models in `main/models.py`
- Adding user authentication and authorization
- Building RESTful APIs with Django REST Framework
- Integrating with frontend frameworks
- Adding more views and templates
- Deploying to production servers

## Development

- **Add new views**: Edit `main/views.py`
- **Add new URLs**: Edit `main/urls.py`
- **Create templates**: Add HTML files in `main/templates/main/`
- **Modify settings**: Edit `ort_project/settings.py`

## Security Notes

⚠️ **Important for Production Deployment:**

This project is configured for development. Before deploying to production:

1. **Change SECRET_KEY**: Generate a new secret key and store it in environment variables
   ```python
   import os
   SECRET_KEY = os.environ.get('SECRET_KEY')
   ```

2. **Disable DEBUG**: Set `DEBUG = False` in settings.py

3. **Configure ALLOWED_HOSTS**: Add your domain to `ALLOWED_HOSTS`

4. **Use HTTPS**: Enable SSL/HTTPS settings (SECURE_SSL_REDIRECT, SECURE_HSTS_SECONDS, etc.)

5. **Use Production Database**: Switch from SQLite to PostgreSQL or MySQL

6. **Configure Static Files**: Set up proper static file serving

For more information, see [Django's deployment checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/).

## License

This project is open source and available for use and modification.
