from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship, column_property

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    name = column_property(first_name + " " + last_name)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    fines = relationship("Fine", backref="user")
    savings = relationship("Saving", backref="user")
    loans = relationship("Loan", backref="user")
