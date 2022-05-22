from typing import Any, Dict, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Instalment, Loan
from app.schemas.instalment import InstalmentCreate, InstalmentUpdate


def update_loan(db: Session, loan_db_obj: Loan, principal: int) -> None:
    loan_db_obj.amount_paid += principal
    loan_db_obj.balance -= principal

    db.add(loan_db_obj)
    db.commit()


class CRUDInstalment(CRUDBase[Instalment, InstalmentCreate, InstalmentUpdate]):
    def create(
        self, db: Session, *, obj_in: InstalmentCreate, loan_db_obj: Loan
    ) -> Instalment:
        update_loan(db, loan_db_obj=loan_db_obj, principal=obj_in.principal)
        db_obj = Instalment(
            date_paid=obj_in.date_paid,
            month=obj_in.month,
            amount=obj_in.amount,
            principal=obj_in.principal,
            interest=obj_in.interest,
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


instalment = CRUDInstalment(Instalment)
