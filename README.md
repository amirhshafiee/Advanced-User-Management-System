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
   1. python -m venv venv

   2. source venv/bin/activate  # On Windows use venv\Scripts\activate

   3. Install dependencies:
            pip install -r requirements.txt

   4. Apply migrations:
            python manage.py migrate

   5. Create a superuser:
            python manage.py createsuperuser

   6. Run the server:
            python manage.py runserver
   ```

## API Endpoints

The project provides the following API endpoints:

### Authentication

- POST /accounts/register/ - Register a new user
- POST /accounts/register/sent-otp-agin/ - Send OTP again
- POST /accounts/register/verify-otp/ - Verify OTP
- 
- POST /accounts/login/ - Login user
- POST /accounts/login/refresh/ - Send new access token with refresh token
- 
- POST /accounts/logout/ - Logout user
- 
- POST /accounts/password/forget/ - Forget password
- POST /accounts/password/forget/verify/ - Verify OPT for forget password
- POST /accounts/password/reset/ - Set new password
- 
- Get /accounts/profile/ - Get user details
- PATCH /accounts/profile/ - Update user information
- POST /accounts/profile/password-reset/ - Change password in profile

### User Management

- GET /admin/users/ - Get a list of users (admin only)
- GET /admin/users/<str:email>/ - Get user details
- PATCH /admin/users/<str:email>/ - Update user information
- GET /admin/actions/ - Get list of users actions

## Configuration

- Modify config/settings.py to change database settings, authentication backends, and other configurations.

## License

This project is licensed under the MIT License.

## Contributors

- Amir Hosien

## Contact

For any inquiries, feel free to reach out at amirshafiee266@yahoo.com.
