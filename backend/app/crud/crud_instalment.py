from typing import Any, Dict, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Instalment, Loan
from app.schemas.instalment import InstalmentCreate, InstalmentUpdate


class CRUDInstalment(CRUDBase[Instalment, InstalmentCreate, InstalmentUpdate]):
    def create(
        self, db: Session, *, obj_in: InstalmentCreate, loan_db_obj: Loan
    ) -> Instalment:
        interest: float = loan_db_obj.balance * (loan_db_obj.interest_rate / 100)
        principal = obj_in.amount - interest
        self.update_loan(db, loan=loan_db_obj, principal=principal, month=obj_in.month)
        db_obj = Instalment(
            date_paid=obj_in.date_paid,
            month=obj_in.month,
            amount=obj_in.amount,
            principal=principal,
            interest=interest,
            loan_id=obj_in.loan_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Instalment,
        obj_in: Union[InstalmentUpdate, Dict[str, Any]]
    ) -> Instalment:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    @staticmethod
    def update_loan(db: Session, loan: Loan, principal: int, month: int) -> None:
        loan.amount_paid += principal
        loan.balance -= principal
        # todo: fix this with say a daemon?
        # loan.remaining_period -= month
        db.add(loan)
        db.commit()


instalment = CRUDInstalment(Instalment)
