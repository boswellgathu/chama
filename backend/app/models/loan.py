from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class Loan(Base):
    id = Column(Integer, primary_key=True, index=True)
    date_acquired = Column(DateTime(timezone=True), server_default=func.now())
    amount = Column(Float, nullable=False)
    interest_rate = Column(Integer, default=10)
    paid = Column(Float)
    balance = Column(Float)
    period = Column(Integer, default=6)
    remaining_period = Column(Integer, default=6)
    status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    member_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    instalments = relationship("Instalment", backref="user")
