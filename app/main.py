from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import Course, Student, StudentCourse
from app.schemas.student import StudentCreate
from app.schemas.course import CourseCreate


app = FastAPI()

@app.get("/")
def root():
    return{"message": "Student management API is running"}


#CREATING STUDENTS

@app.post("/students")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(
        name = student.name,
        email = student.email,
        phone = student.phone,
        date_of_birth=student.date_of_birth
    )

    db.add(new_student)
    try:
        db.commit()
        db.refresh(new_student)

    except IntegrityError:
        db.rollback()

        raise HTTPException(status_code=409,detail="Email already exists")

    return new_student


#Get student by ID

@app.get("/students/{student_id}")
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if student is None:raise HTTPException(status_code=404,detail="Student not found")

    return student


# CREATING COURSES

@app.post("/courses")
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    new_course = Course(
        course_name = course.course_name,
        description = course.description
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


#READING ALL COURSES

@app.get("/courses")
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses

#Getting course by ID

@app.get("/courses/{course_id}")
def get_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    course = (
        db.query(Course)
        .filter(Course.id == course_id)
        .first()
    )

    if course is None:raise HTTPException(status_code=404,detail="Course not found")

    return course


@app.post("/students/{student_id}/courses/{course_id}")
def enroll_student(
    student_id: int,
    course_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:raise HTTPException(status_code=404,detail="Student not found")

    course = db.query(Course).filter(Course.id == course_id).first()

    if course is None:raise HTTPException(status_code=404,detail="Course not found")

    enrollment = StudentCourse(
        student_id=student_id,
        course_id=course_id
    )

    db.add(enrollment)

    try:
        db.commit()
        db.refresh(enrollment)

    except IntegrityError:
        db.rollback()

        raise HTTPException(status_code=409,detail="Student is already enrolled in this course")

    return enrollment




@app.get("/students/{student_id}/courses")
def get_student_courses(student_id: int,db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404,detail="Student not found")

    courses = (db.query(Course).join(StudentCourse, Course.id == StudentCourse.course_id).filter(StudentCourse.student_id == student_id).all())

    return courses




#Updating a course

@app.put("/courses/{course_id}")
def update_course(
    course_id: int,
    course: CourseCreate,
    db: Session = Depends(get_db)
):
    existing_course = (db.query(Course).filter(Course.id == course_id).first())

    if existing_course is None:raise HTTPException(status_code=404,detail="Course not found")

    existing_course.course_name = course.course_name
    existing_course.description = course.description

    db.commit()
    db.refresh(existing_course)

    return existing_course


#Deleting a course

@app.delete("/courses/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    course = (db.query(Course).filter(Course.id == course_id).first())

    if course is None:
        raise HTTPException(status_code=404,detail="Course not found")

    db.query(StudentCourse).filter(StudentCourse.course_id == course_id).delete()

    db.delete(course)
    db.commit()

    return {
        "message": "Course deleted successfully"
    }


#Deleting a student

@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = (db.query(Student).filter(Student.id == student_id).first())

    if student is None:raise HTTPException(status_code=404,detail="Student not found")

    db.query(StudentCourse).filter(
        StudentCourse.student_id == student_id
    ).delete()

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully"
    }

##Get all students

@app.get("/students")
def get_students(
    db: Session = Depends(get_db)
):
    students = db.query(Student).all()

    return students



#Update student

@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    existing_student = (db.query(Student).filter(Student.id == student_id).first())

    if existing_student is None:raise HTTPException(status_code=404,detail="Student not found")

    existing_student.name = student.name
    existing_student.email = student.email
    existing_student.phone = student.phone
    existing_student.date_of_birth = student.date_of_birth

    db.commit()
    db.refresh(existing_student)

    return existing_student