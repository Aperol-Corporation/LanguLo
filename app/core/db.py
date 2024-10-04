from sqlalchemy.ext.declarative import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    def to_dict(self):
        return {
            field.name: getattr(self, field.name) for field in self.__table__.c
        }
