from flask_bcrypt import Bcrypt

from api.models.base import Base, db



class User(Base):
    """Models Users."""

    __tablename__ = 'users'

    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    businesses = db.relationship(
        'Business',
        backref='created_by',
        lazy='dynamic',
        order_by='desc(Business.created_at)'
    )
    transactions = db.relationship(
        'Transaction',
        backref='created_by',
        lazy='dynamic',
        cascade="all, delete-orphan"
    )

    def __init__(self, first_name, last_name, email, password):
        """
        Initialization of user credentials
        """

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()
