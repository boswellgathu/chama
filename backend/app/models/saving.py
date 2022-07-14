from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Date,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

from app.db.base_class import Base


class Saving(Base):
    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    date_sent = Column(Date, nullable=False)
    is_late = Column(Boolean(), default=False)
    fine_id = Column(Integer, ForeignKey("fine.id"), nullable=True)
    member_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    fine = relationship("Fine", backref=backref("saving", uselist=False))

    __table_args__ = (
        UniqueConstraint("month", "year", "member_id", name="month_year_user_unique"),
    )
