# CortexSys-TODO
The CortexSys TODO Project is a lightweight yet robust task management API designed to help
users efficiently organize and track their daily activities. It provides a clean, fast, and secure
backend for task management, optimized for individual and small team productivity.

## Features
- Create, edit, and delete tasks
- Mark tasks as completed or pending
- Filter tasks by status or priority
- Simple and intuitive API endpoints for task handling
- User authentication and secure task access

## Technologies Used
- Backend: Django REST Framework
- Database: PostgreSQL
- Authentication: JWT (JSON Web Token)
- Testing: pytest (each app has its own test suite)
- Deployment (Optional): Docker containers
- Optional Tools: Django Admin for backend management

## Database Models Overview
- User: Custom user model for authentication.
- Task: Fields include title, description, status, due_date, priority, user, created_at, updated_at.

## UML Diagram
+----------------+ 1 * +----------------+
| User |---------------------->| Task |
+----------------+ +----------------+
| id | | id |
| username | | title |
| email | | description |
| password | | status |
+----------------+ | due_date |
| priority |
| user_id (FK) |
+----------------+

## Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd CortexSys-TODO
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the root directory:
```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=the_allowed_host
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=the_db_host
DB_PORT=5432
```

### 5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser
```bash
python manage.py createsuperuser
```

### 7. Run the development server
```bash
python manage.py runserver
```

## API Endpoints

- POST /api/auth/register/ -- Register new user
- POST /api/auth/login/ -- Login and get JWT token
- GET /api/tasks/ -- List user tasks
- POST /api/tasks/ -- Create new task
- PUT /api/tasks/id/ -- Update task
- DELETE /api/tasks/id/ -- Delete task

## Testing

### Django tests
```bash
python manage.py test
```
OR
```bash
pytest <test-file>
```

## Project Structure
```
CortexSys-TODO/
    cortexsys_todo/
        manage.py
        accounts/
            models.py
            managers.py
            serializers.py
            views.py
            permissions.py
            tests/
        tasks/
            models.py
            serializers.py
            views.py
            tests/
        cortexsys_todo/
            settings.py
            urls.py
```

## License
MIT
