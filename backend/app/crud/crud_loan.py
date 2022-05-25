from typing import Any, Dict, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.loan import Loan
from app.schemas.loan import LoanCreate, LoanInDB, LoanStatus, LoanUpdate


class CRUDLoan(CRUDBase[Loan, LoanCreate, LoanUpdate]):
    def create(self, db: Session, *, obj_in: LoanCreate) -> LoanInDB:
        db_obj = Loan(
            date_acquired=obj_in.date_acquired,
            amount=obj_in.amount,
            interest_rate=obj_in.interest_rate,
            amount_paid=obj_in.amount_paid,
            balance=obj_in.amount,
            period=obj_in.period,
            member_id=obj_in.member_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Loan, obj_in: Union[LoanUpdate, Dict[str, Any]]
    ) -> Loan:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        loan_amount = update_data.get("amount")
        if loan_amount:
            update_data["balance"] = loan_amount
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    @staticmethod
    def is_previous_loan_paid(db: Session, member_id: int) -> bool:
        previous_unpaid_loan = (
            db.query(Loan).filter_by(member_id=member_id).filter(Loan.balance != 0.0)
        ).first()

        if previous_unpaid_loan:
            return False
        return True

    @staticmethod
    def restructure(
        db: Session, db_obj: Loan, obj_in: Union[LoanUpdate, Dict[str, Any]]
    ) -> Loan:
        pass
        # create new loan
        new_loan = Loan(
            date_acquired=db_obj.date_acquired,
            amount=obj_in.amount,
            interest_rate=db_obj.interest_rate,
            balance=obj_in.amount,
            period=db_obj.period,
            member_id=db_obj.member_id,
        )
        db.add(new_loan)
        db.commit()

        # update current with status restructured
        db_obj.restructured_to_id = new_loan.id
        db_obj.status = LoanStatus.RESTRUCTURED

        db.add(db_obj)
        db.commit()

        db.refresh(new_loan)
        return new_loan


loan = CRUDLoan(Loan)
