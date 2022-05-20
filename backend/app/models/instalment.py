from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func

from app.db.base_class import Base


class Saving(Base):
    id = Column(Integer, primary_key=True, index=True)
    date_paid = Column(DateTime(timezone=True), server_default=func.now())
    month = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    principal = Column(Float)
    interest = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    loan_id = Column(Integer, ForeignKey("loan.id"), nullable=False)
