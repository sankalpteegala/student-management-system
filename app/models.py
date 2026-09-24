from datetime import datetime, date

from sqlalchemy import String, Text, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base




class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    course_name : Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable= True)
    student_courses: Mapped[list["StudentCourse"]] = relationship(back_populates="course")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)




class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable= False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=True)
    courses: Mapped[list["StudentCourse"]] = relationship(back_populates="student")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

class StudentCourse(Base):
    __tablename__ = "student_courses"

    __table_args__ = (UniqueConstraint("student_id","course_id",name="uq_student_course"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"),nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"),nullable=False)
    student: Mapped["Student"] = relationship(back_populates="courses")
    course: Mapped["Course"] = relationship(back_populates="student_courses")