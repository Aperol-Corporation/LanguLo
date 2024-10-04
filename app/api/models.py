from enum import Enum

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constance import CATEGORY_NAME_LENGTH, STRING_LENGTH
from app.core.db import Base


class SpeakingSkillEnum(str, Enum):
    begginer = 'begginer'
    pre_intermidiate = 'pre-intermidiate'
    intermidiate = 'intermidiate'
    pre_advanced = 'pre-advanced'
    advanced = 'advanced'
    native = 'native'


class TagsEnum(str, Enum):
    pronunciation = 'pronunciation'
    speaking = 'speaking'
    comprehension = 'comprehension'
    listenig = 'listenig'
    writing = 'writing'
    reading = 'reading'


class DurationEnum(str, Enum):
    thirry_minutes = 30
    fourty_five_minutes = 45
    sixty_minutes = 60
    ninty_minutes = 90


class Languages(Base):
    """Model for all languages available."""

    __tablename__ = 'languages'

    name: Mapped[str] = mapped_column(String(STRING_LENGTH), unique=True)


class SpokenLanguage(Base):
    """Model for languages that users can speak."""

    __tablename__ = 'spoken_languages'

    name: Mapped['Languages'] = mapped_column(ForeignKey('language'))
    speaking_skill: Mapped[SpeakingSkillEnum] = mapped_column(String)
    comprehension_skill: Mapped[SpeakingSkillEnum] = mapped_column(String)
    listenig_skill: Mapped[SpeakingSkillEnum] = mapped_column(String)
    writing_skill: Mapped[SpeakingSkillEnum] = mapped_column(String)
    reading_skill: Mapped[SpeakingSkillEnum] = mapped_column(String)


class Category(Base):
    """Model for lesson's category, purpose of the class."""

    __tablename__ = 'categories'

    name: Mapped[str] = mapped_column(String(CATEGORY_NAME_LENGTH))
    price: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String)
    tags: Mapped[TagsEnum] = mapped_column(String)
    language_level: Mapped[list[SpeakingSkillEnum]] = mapped_column(String)
    lessons: Mapped[list['Lesson']] = relationship(
        secondary='categories_lessons', back_populates='categories'
    )


class Lesson(Base):
    """Model for reserved or finished class."""

    __tablename__ = 'lessons'

    # platform
    teacher: Mapped['Teacher'] = mapped_column(ForeignKey('lessons'))
    student: Mapped['Student'] = mapped_column(ForeignKey('lessons'))
    category: Mapped[list['Category']] = relationship(
        secondary='lessons_categories', back_populates='lessons'
    )
    duration: Mapped[DurationEnum] = mapped_column(Integer)
