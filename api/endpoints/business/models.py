from api.models.base import Base, db


class Business(Base):
    """Model Business"""

    __tablename__ = "businesses"

    name = db.Column(db.String, nullable=False)
    abbreviated_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    entity = db.Column(db.String, nullable=False)
    revenue = db.Column(db.String, nullable=False)
    accounting_software = db.Column(db.String, nullable=False)
    op_countries = db.relationship(
        'Country',
        backref='business',
        lazy='dynamic',
        cascade="all, delete-orphan"
    )
    transactions = db.relationship(
        'Transaction',
        backref='business',
        lazy='dynamic',
        cascade="all, delete-orphan"
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


class Transaction(Base):
    """Model Transaction"""

    __tablename__ = "transations"

    item = db.Column(db.String, default="", nullable=False)
    transaction_type = db.Column(db.String, default="", nullable=False)
    transaction_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, default="", nullable=False)
    transaction_date = db.Column(db.String, default="", nullable=False)
    due_date = db.Column(db.String, default="", nullable=False)
    customer_or_supplier = db.Column(db.String, default="", nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)
    unit_amount = db.Column(db.Float, default=0.0, nullable=False)
    transaction_amount = db.Column(db.Float, default=0.0, nullable=False)
    business_id = db.Column(
        db.String,
        db.ForeignKey('businesses.uuid'),
        nullable=False
    )
    created_by_id = db.Column(
        db.String,
        db.ForeignKey('users.uuid'),
        nullable=False
    )

