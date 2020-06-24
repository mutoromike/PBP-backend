from api.models.base import Base, db



class User(Base):
    """Models Users."""

    __tablename__ = 'users'

    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    # businesses = db.relationship(
    #     'Business',
    #     backref='created_by',
    #     lazy='dynamic',
    #     order_by='desc(Business.created_at)'
    # )
