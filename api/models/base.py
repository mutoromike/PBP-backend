"""Contain All App Models."""
import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError


db = SQLAlchemy()

def generate_uuid():
    """Generate unique string."""
    return str(uuid.uuid1())


def camel_case(snake_str):
    """Convert string to camel case."""
    title_str = snake_str.title().replace("_", "")

    return title_str[0].lower() + title_str[1:]


class Base(db.Model):
    """Base model, contain utility methods and properties."""

    __abstract__ = True
    uuid = db.Column(db.String, primary_key=True, default=generate_uuid)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def save(self):
        """Save the object in DB.

        Return:
            saved(boolean) true if saved, false otherwise
        """
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    def delete(self):
        """Delete the object in DB.

        Return
            deleted(boolean) True if deleted else false
        """
        deleted = None
        try:
            db.session.delete(self)
            db.session.commit()
            deleted = True
        except Exception:
            deleted = False
            db.session.rollback()
        return deleted

    def serialize(self):
        """Map model to a dictionary representation.

        Return:
            A dict object
        """
        dictionary_mapping = {
            camel_case(attribute.name): str(getattr(self, attribute.name))
            if not isinstance(getattr(self, attribute.name), int)
            else getattr(self, attribute.name)
            for attribute in self.__table__.columns
        }
        return dictionary_mapping
