# HomeTutor

HomeTutor is an online tuition media platform where students and tutors can connect. It is built using **Django Rest Framework (DRF)** and uses **Djoser** for authentication.

## Features
- **User & Tutor Management**:
  - Separate registration and login for students (Users).
  - Separate registration and login for tutors.
- **JWT Authentication**: Authentication system based on **JWT Token** using **Djoser**.
- **Email Verification**: Email verification for both users and tutors.
- **API Documentation**: API documentation through **Swagger UI** using **drf_yasg**.

## Installation
### Prerequisites
- Python 3.x
- Django
- Django Rest Framework
- Djoser
- drf_yasg

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/HomeTutor.git
cd HomeTutor

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # (For Windows, use `venv\\Scripts\\activate`)

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser

# Run the server
python manage.py runserver

```
### API Documentation

You can view the API documentation via Swagger UI at the following URL:
```
http://127.0.0.1:8000/swagger/
```

## Environment Variables

To run this project, you need to configure the following environment variables:

- `DJANGO_SECRET_KEY`: The secret key used by Django for cryptographic signing.
- `EMAIL_BACKEND`: The email backend to use (e.g., `django.core.mail.backends.smtp.EmailBackend`).
- `EMAIL_HOST`: The host to use for sending email (e.g., `smtp.gmail.com`).
- `EMAIL_PORT`: The port to use for the email server (e.g., `587`).
- `EMAIL_HOST_USER`: The email address used for sending emails.
- `EMAIL_HOST_PASSWORD`: The email account's password.


## License
This project is licensed under the **MIT License**.

---

**Developed by Partho Kumar Mondal** 