from typing import Any, Dict
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from app.settings.database.mixins import AllFeaturesMixin
from app.settings.database import SessionScoped


# class CustomBase(object):
#     # Generate __tablename__ automatically
#     @declared_attr
#     def __tablename__(cls):
#         return cls.__name__.lower()

# DeclarativeBase = declarative_base(cls=CustomBase)


@as_declarative()
class BaseClass:
    id: Any
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

# Enhanced Base Model Class with some django-like super powers
class Base(BaseClass, AllFeaturesMixin):
    __abstract__ = True

    @classmethod
    def all_by_page(cls, page: int = 1, limit: int = 20, **kwargs) -> Dict:
        start = (page - 1) * limit
        end = start + limit
        return cls.query.slice(start, end).all()

    @classmethod
    def get(cls, **kwargs) -> Dict:
        """Return the the first value in database based on given args.
        Example:
            User.get(id=5)
        """
        return cls.where(**kwargs).first()


Base.set_session(SessionScoped())