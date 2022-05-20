from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class FineReason(str, Enum):
    SavingsFine = "SAVINGSFINE"
    LoanFine = "LOANFINE"
    MeetingFine = "MEETINGFINE"


class FineBase(BaseModel):
    amount: int
    reason: FineReason = FineReason.SavingsFine
    paid: bool = False
    member_id: int


class FineCreate(FineBase):
    pass


class FineUpdate(FineCreate):
    amount: None | int
    reason: None | FineReason
    paid: bool
    member_id: None | int


class FineInDBBase(FineCreate):
    id: int | None = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Fine(FineInDBBase):
    pass


# Additional properties stored in DB
class FineInDB(FineInDBBase):
    created_at: datetime
    updated_at: datetime
