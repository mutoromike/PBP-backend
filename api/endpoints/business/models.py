from api.models.base import Base, db


class Business(Base):
    """Model Business"""

    __tablename__ = "businesses"

    name = db.Column(db.String, nullable=False)
    name_abbr = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    entity = db.Column(db.String, nullable=False)
    revenue = db.Column(db.String, nullable=False)
    acc_sftw = db.Column(db.String, nullable=False)
    op_countries = db.relationship(
        'Country',
        backref='business',
        lazy='dynamic'
    )
    created_by_id = db.Column(
        db.String,
        db.ForeignKey('users.uuid'),
        nullable=False
    )


class Country(Base):
    """Model Country"""

    __tablename__ = "countries"

    name = db.Column(db.String, nullable=False)
    business_id = db.Column(
        db.String,
        db.ForeignKey('businesses.uuid'),
        nullable=False
    )