# Django Backend Project

## Description

This is a backend project built using Django. It includes an authentication system and user management functionalities.

## Features

- User authentication (registration, login, logout)
- JWT-based authentication
- Django REST Framework for API development
- SQLite as the database (default, can be changed)

## Installation

### Prerequisites

Ensure you have the following installed:

- Python (>=3.8)
- pip
- virtualenv (optional but recommended)

### Steps

1. Clone the repository:
   sh
   git clone <repository-url>
   cd Back-End
   
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   3. Install dependencies:
   sh
   pip install -r requirements.txt
   4. Apply migrations:
   sh
   python manage.py migrate
   5. Create a superuser:
   sh
   python manage.py createsuperuser
   6. Run the server:
   sh
   python manage.py runserver
   ```

## API Endpoints

The project provides the following API endpoints:

### Authentication

- POST /api/auth/register/ - Register a new user
- POST /api/auth/login/ - Login and obtain JWT
- POST /api/auth/logout/ - Logout user

### User Management

- GET /api/users/ - Get a list of users (admin only)
- GET /api/users/<id>/ - Get user details
- PUT /api/users/<id>/ - Update user information
- DELETE /api/users/<id>/ - Delete user

## Configuration

- Modify config/settings.py to change database settings, authentication backends, and other configurations.

## License

This project is licensed under the MIT License.

## Contributors

- [Your Name]

## Contact

For any inquiries, feel free to reach out at [your-email\@example.com].
