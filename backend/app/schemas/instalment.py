from datetime import date, datetime
from pydantic import BaseModel


class InstalmentBase(BaseModel):
    date_paid: date
    month: int
    amount: float
    loan_id: int


class InstalmentCreate(InstalmentBase):
    pass


class InstalmentUpdate(InstalmentCreate):
    date_paid: None | date
    month: None | int
    amount: None | float
    loan_id: None | int


class InstalmentInDBBase(InstalmentCreate):
    id: int | None = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Instalment(InstalmentInDBBase):
    principal: float
    interest: float


# Additional properties stored in DB
class InstalmentInDB(InstalmentInDBBase):
    created_at: datetime
    updated_at: datetime
