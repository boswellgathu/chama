from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel


class Month(str, Enum):
    JANUARY = "JANUARY"
    FEBRUARY = "FEBRUARY"
    MARCH = "MARCH"
    APRIL = "APRIL"
    MAY = "MAY"
    JUNE = "JUNE"
    JULY = "JULY"
    AUGUST = "AUGUST"
    SEPTEMBER = "SEPTEMBER"
    OCTOBER = "OCTOBER"
    NOVEMBER = "NOVEMBER"
    DECEMBER = "DECEMBER"


class SavingBase(BaseModel):
    date_sent: date  # date the member sent their saving.
    month: Month
    year: int = datetime.now().year
    amount: int
    is_late: bool = False
    member_id: int
    fine_id: int | None = None


class SavingCreate(SavingBase):
    pass


class SavingUpdate(SavingCreate):
    date_sent: None | date  # date the member sent their saving.
    month: None | Month
    amount: None | int
    member_id: None | int


class SavingInDBBase(SavingCreate):
    id: int | None = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Saving(SavingInDBBase):
    pass


# Additional properties stored in DB
class SavingInDB(SavingInDBBase):
    created_at: datetime
    updated_at: datetime


class AllSavings(BaseModel):
    name: str
    year: int
    month: str
    date_sent: date
    is_late: bool
    fined: bool
    fine_amount: float
    fine_paid: bool
