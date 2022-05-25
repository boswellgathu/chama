from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

from app.db.base_class import Base


class Loan(Base):
    id = Column(Integer, primary_key=True, index=True)
    date_acquired = Column(DateTime(timezone=True), server_default=func.now())
    amount = Column(Float, nullable=False)
    interest_rate = Column(Integer, default=10)
    amount_paid = Column(Float, default=0.0)
    balance = Column(Float)
    period = Column(Integer, default=6)
    remaining_period = Column(Integer, default=6)
    status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    member_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    restructured_to_id = Column(Integer, ForeignKey("loan.id"), nullable=True)
    instalments = relationship("Instalment", backref="user")
    restructures = relationship("Loan", backref=backref("loan", remote_side=[id]))
