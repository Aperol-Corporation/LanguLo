from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy_file import FileField

from core.constants import (
    CERTIFICATE_LENGTH,
    DESCRIPTION_LENGTH,
    EMAIL_LENGTH,
    FIRST_NAME_LENGTH,
    LAST_NAME_LENGTH,
    LOCATION_NAME_LENGTH
)
from core.enums import PlatformEnum, RoleEnum


class Base(DeclarativeBase):
    """Base class for models."""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp()
    )

    def to_dict(self):
        return {
            field.name: getattr(self, field.name) for field in self.__table__.c
        }


class SpokenBy(Base):
    """Abstract model for through models utilizing SpokenLanguage."""

    id = None
    language_id: Mapped[int] = mapped_column(
        ForeignKey('spoken_languages.id'), primary_key=True
    )


class User(Base):
    """Abstract User model."""

    email: Mapped[str] = mapped_column(String(EMAIL_LENGTH), unique=True)
    first_name: Mapped[str] = mapped_column(String(FIRST_NAME_LENGTH))
    last_name: Mapped[str] = mapped_column(String(LAST_NAME_LENGTH))
    role: Mapped[RoleEnum]
    # TODO: Add wallet: WalletModel


class AdminUser(User):  # TODO: Very complicated, figure out later
    """Модель Админа."""

    __tablename__ = 'admin_users'

    last_login: Mapped[datetime] = mapped_column(nullable=True)

    def __repr__(self):
        return f'<Admin User {self.first_name} {self.last_name}>'


class Teacher(User):
    """Teacher model."""

    __tablename__ = 'teachers'

    teaches: Mapped[list['Language']] = relationship(
        secondary='taught_by_teachers', back_populates='taught_by'
    )
    speaks: Mapped[list['SpokenLanguage'] | None] = relationship(
        secondary='spoken_by_teachers', back_populates='spoken_by_teachers'
    )
    platform: Mapped[PlatformEnum]
    location: Mapped[str] = mapped_column(String(LOCATION_NAME_LENGTH))
    preview_video: Mapped[FileField] = mapped_column(FileField)
    topics: Mapped[int] = mapped_column(ForeignKey('topics.id'))
    description: Mapped[str] = mapped_column(String(DESCRIPTION_LENGTH))
    certificate: Mapped[str] = mapped_column(String(CERTIFICATE_LENGTH))
    students: Mapped[list['Student']] = relationship(
        secondary='students_teachers', back_populates='teachers'
    )
    courses: Mapped['Course'] = mapped_column(ForeignKey('courses.id'))
    number_of_lessons: Mapped[int]

    def __repr__(self):
        return f'<Teacher: {self.id} | {self.name}>'


class Student(User):
    """Student model."""

    __tablename__ = 'students'

    learns: Mapped[list['Language'] | None] = relationship(
        secondary='learnt_by_students', back_populates='learnt_by'
    )
    speaks: Mapped[list['SpokenLanguage']] = relationship(
        secondary='spoken_by_students', back_populates='spoken_by_students'
    )
    teachers: Mapped[list['Teacher']] = relationship(
        secondary='students_teachers', back_populates='students'
    )

    def __repr__(self):
        return f'<Student: {self.id} | {self.name}>'


class StudentsTeachers(Base):
    """Through model for Student-Teacher relationship."""
    __tablename__ = 'students_teachers'

    id = None
    student_id: Mapped[int] = mapped_column(
        ForeignKey('students.id'), primary_key=True
    )
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey('teachers.id'), primary_key=True
    )

    def __repr__(self):
        return f'<Student {self.student_id} ~ Teacher {self.teacher_id}>'


class TaughtByTeachers(Base):
    """
    Through model for Language-Teacher relationship.
    Maps to languages that the teacher teaches.
    """

    __tablename__ = 'taught_by_teachers'

    id = None
    language_id: Mapped[int] = mapped_column(
        ForeignKey('languages.id'), primary_key=True
    )
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey('teachers.id'), primary_key=True
    )

    def __repr__(self):
        return f'<Language {self.language_id} ~ Teacher {self.teacher_id}>'


class SpokenByTeachers(SpokenBy):
    """
    Through model for SpokenLanguage-Teacher relationship.
    Maps to languages that the teacher can speak (i.e. to SpokenLanguage)
    """

    __tablename__ = 'spoken_by_teachers'

    teacher_id: Mapped[int] = mapped_column(
        ForeignKey('teachers.id'), primary_key=True
    )

    def __repr__(self):
        return (
            f'<SpokenLanguage {self.language_id} ~ Teacher {self.teacher_id}>'
        )


class LearntByStudents(Base):
    """
    Through model for Language-Student relationship.
    Maps to languages that the student learns.
    """

    __tablename__ = 'learnt_by_students'

    id = None
    language_id: Mapped[int] = mapped_column(
        ForeignKey('languages.id'), primary_key=True
    )
    student_id: Mapped[int] = mapped_column(
        ForeignKey('students.id'), primary_key=True
    )

    def __repr__(self):
        return f'<Language {self.language_id} ~ Student {self.student_id}>'


class SpokenByStudents(SpokenBy):
    """
    Through model for SpokenLanguage-Student relationship.
    Maps to languages that the student can speak (i.e. to SpokenLanguage)
    """

    __tablename__ = 'spoken_by_students'

    student_id: Mapped[int] = mapped_column(
        ForeignKey('students.id'), primary_key=True
    )

    def __repr__(self):
        return (
            f'<SpokenLanguage {self.language_id} ~ Student {self.student_id}>'
        )
