# Student Management System

A RESTful Student Management API built with FastAPI, PostgreSQL, SQLAlchemy and Alembic.

This project demonstrates backend API development with database integration, CRUD operations, many-to-many relationships, validation, transaction handling, error handling and database migrations.

## Features

- Create, retrieve, update and delete students
- Create, retrieve, update and delete courses
- Enroll students in courses
- Retrieve all courses enrolled by a student
- Prevent duplicate student-course enrollments
- PostgreSQL database integration
- SQLAlchemy ORM for database operations
- Alembic database migrations
- Dependency injection for database sessions
- HTTP error handling with appropriate status codes
- Automatic API documentation with Swagger UI

## Tech Stack

- **Python 3.12**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy 2.0**
- **Pydantic**
- **Alembic**
- **Uvicorn**
- **Psycopg 3**

## Project Structure

```text
student_managment_system/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   │
│   └── schemas/
│       ├── student.py
│       └── course.py
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── alembic.ini
├── .gitignore
└── README.md

Database Design

The application uses three main tables.

Students

Stores student information:

ID
Name
Email
Phone
Date of Birth
Created At
Updated At
Courses

Stores:

ID
Course Name
Description
Created At
Student Courses

student_courses is an association table that implements the many-to-many relationship between students and courses.

Student
   │
   │ 1
   │
   │ *
StudentCourse
   │
   │ *
   │
   │ 1
   │
Course

A student can enroll in multiple courses, and a course can have multiple students.

A unique constraint on (student_id, course_id) prevents the same student from being enrolled in the same course more than once.

API Endpoints
Students
Method	Endpoint	Description
POST	/students	Create a student
GET	/students	Get all students
GET	/students/{student_id}	Get a student by ID
PUT	/students/{student_id}	Update a student
DELETE	/students/{student_id}	Delete a student
Courses
Method	Endpoint	Description
POST	/courses	Create a course
GET	/courses	Get all courses
GET	/courses/{course_id}	Get a course by ID
PUT	/courses/{course_id}	Update a course
DELETE	/courses/{course_id}	Delete a course
Student-Course Relationships
Method	Endpoint	Description
POST	/students/{student_id}/courses/{course_id}	Enroll a student in a course
GET	/students/{student_id}/courses	Get courses for a student
API Documentation

FastAPI automatically provides interactive API documentation through Swagger UI.

After starting the application, open:

http://127.0.0.1:8000/docs

The Swagger interface allows you to test the API endpoints directly from the browser.

Database Migrations

Alembic is used to manage database schema changes.

Create a new migration:

alembic revision --autogenerate -m "migration message"

Apply migrations:

alembic upgrade head

Check the current migration:

alembic current

View migration history:

alembic history
Running the Project Locally
1. Clone the repository
git clone https://github.com/sankalpteegala/student-management-system.git
cd student-management-system
2. Create a virtual environment
python3.12 -m venv .venv

Activate it:

source .venv/bin/activate
3. Install dependencies
pip install fastapi sqlalchemy psycopg pydantic uvicorn alembic
4. Configure PostgreSQL

Create a PostgreSQL database named:

student_management

Update the PostgreSQL connection details in:

app/database.py
5. Apply database migrations
alembic upgrade head
6. Start the API
python -m uvicorn app.main:app --reload

The API will be available at:

http://127.0.0.1:8000

Swagger UI:

http://127.0.0.1:8000/docs
Example Requests
Create a Student
POST /students
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "9876543210",
  "date_of_birth": "2001-05-15"
}
Enroll a Student
POST /students/1/courses/2

This creates a relationship between student 1 and course 2.

Error Handling

The API handles common application errors using appropriate HTTP status codes, including:

404 Not Found when a requested student or course does not exist
409 Conflict when attempting to create a duplicate student email or duplicate course enrollment

Database transactions are rolled back when an integrity error occurs.

What I Learned

Through this project, I practiced:

Building REST APIs with FastAPI
Designing relational database schemas
Working with PostgreSQL
Using SQLAlchemy ORM
Implementing many-to-many relationships
Managing database sessions with dependency injection
Handling database transactions
Handling API errors
Using Alembic for database migrations
Testing APIs using Swagger UI
Future Improvements

Possible improvements for a production-ready version could include:

Authentication and authorization
Pagination and filtering
Automated testing with Pytest
Docker containerization
Environment-based configuration
API versioning
Logging and monitoring

Built as a backend development project to strengthen practical experience with FastAPI, PostgreSQL and SQLAlchemy.