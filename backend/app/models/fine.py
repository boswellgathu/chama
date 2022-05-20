from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func

from app.db.base_class import Base


class Fine(Base):
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    reason = Column(String, nullable=False)  # needs Enum
    paid = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    member_id = Column(Integer, ForeignKey("user.id"), nullable=False)
