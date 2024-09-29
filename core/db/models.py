from datetime import datetime

from sqlalchemy import func, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy_file import FileField

from core.constants import (
    USERNAME_LENGTH,
    EMAIL_LENGTH,
    FIRST_NAME_LENGTH,
    LAST_NAME_LENGTH,
    PLATFORM_NAME_LENGTH,
    LOCATION_NAME_LENGTH,
    DESCRIPTION_LENGTH,
)


class Base(DeclarativeBase):
    """Base class for models."""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.current_timestamp())

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.c}


class User(Base):
    """Abstract User model."""

    username: Mapped[str] = mapped_column(String(USERNAME_LENGTH), unique=True)
    email: Mapped[str] = mapped_column(String(EMAIL_LENGTH), unique=True)
    first_name: Mapped[str] = mapped_column(String(FIRST_NAME_LENGTH))
    last_name: Mapped[str] = mapped_column(String(LAST_NAME_LENGTH))
    # TODO: Add wallet: WalletModel


class Teacher(User):
    """Teacher model."""

    __tablename__ = "teachers"

    languages_taught: Mapped["Language"] = mapped_column(ForeignKey("languages.id"))

    platform: Mapped[str] = mapped_column(String(PLATFORM_NAME_LENGTH))

    languages_spoken: Mapped["Language"] = mapped_column(ForeignKey("languages.id"))

    location: Mapped[str] = mapped_column(String(LOCATION_NAME_LENGTH))

    preview_video: Mapped[FileField] = mapped_column(FileField)  # Complex config, add later

    # TODO: How to make `topics` field

    description: Mapped[str] = mapped_column(String(DESCRIPTION_LENGTH))

    # TODO: Add `certificate` filefield?

    students: Mapped["Student"] = mapped_column(ForeignKey("students.id"))

    courses: Mapped["Course"] = mapped_column(ForeignKey("courses.id"))

    # TODO: Посмотреть, как реализовать календарь

    def __repr__(self):
        return f"<Teacher: {self.id} | {self.name}>"


class Student(User):
    """Student model."""

    __tablename__ = "students"

    languages_being_learnt: Mapped["Language"] = mapped_column(ForeignKey("languages.id"))
    languages_spoken: Mapped["Language"] = mapped_column(ForeignKey("languages.id"))
    teachers: Mapped["Teacher"] = mapped_column(ForeignKey("teachers.id"))

    def __repr__(self):
        return f"<Student: {self.id} | {self.name}>"
