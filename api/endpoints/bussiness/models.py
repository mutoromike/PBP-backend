from api.models.base import Base, db


class Business(Base):
    """Model Business"""

    __tablename__ = "businesses"

    name = db.Column(db.String, nullable=False)
