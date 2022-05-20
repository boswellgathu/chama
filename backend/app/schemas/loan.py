from enum import Enum
from datetime import date, datetime

from pydantic import BaseModel

class LoanStatus(str, Enum):
    DEFAULTED = "DEFAULTED"
    SERVICED = "SERVICED"
    COMPLETED = "COMPLETED"

class LoanBase(BaseModel):
    date_acquired: date
    amount: int
    paid: None | float = None
    balance: None | float = None
    interest_rate: int = 10
    period: int = 6  # months
    member_id: int


class LoanCreate(LoanBase):
    pass


class LoanUpdate(LoanCreate):
    date_acquired: None | date
    amount: None | int
    paid: float
    balance: float
    member_id: None | int


class LoanInDBBase(LoanCreate):
    id: int | None = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Loan(LoanInDBBase):
    remaining_period: int = 6
    status: None | LoanStatus = None


# Additional properties stored in DB
class LoanInDB(LoanInDBBase):
    created_at: datetime
    updated_at: datetime
