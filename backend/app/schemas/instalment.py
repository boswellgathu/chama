from datetime import date, datetime
from pydantic import BaseModel


class InstallmentBase(BaseModel):
    date_paid: date
    month: int
    amount: float
    loan_id: int


class InstallmentCreate(InstallmentBase):
    pass


class InstallmentUpdate(InstallmentCreate):
    date_paid: None | date
    month: None | int
    amount: None | float
    loan_id: None | int


class InstallmentInDBBase(InstallmentCreate):
    id: int | None = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Installment(InstallmentInDBBase):
    principal: float
    interest: float


# Additional properties stored in DB
class InstallmentInDB(InstallmentInDBBase):
    created_at: datetime
    updated_at: datetime
