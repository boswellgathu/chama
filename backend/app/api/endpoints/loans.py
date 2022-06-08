from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import dependencies as deps
from app.schemas.loan import LoanCreate, LoanUpdate
from app import crud, schemas

router = APIRouter()


@router.get("/")
async def hello():
    return {"message": "hello loans!"}


@router.post("/", response_model=schemas.Loan)
def create_loan(*, db: Session = Depends(deps.get_db), loan_in: LoanCreate) -> Any:
    """
    Create new loan.
    """
    user = crud.user.get(db, id=loan_in.member_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The member whose loan is being added does not exist in the system",
        )

    is_previous_loan_paid = crud.loan.is_previous_loan_paid(
        db, member_id=loan_in.member_id
    )
    if not is_previous_loan_paid:
        raise HTTPException(
            status_code=404,
            detail="This member has another uncompleted(unpaid) loan.",
        )
    loan = crud.loan.create(db, obj_in=loan_in)
    return loan


@router.put("/{loan_id}", response_model=schemas.Loan)
def update_loan(
    *, db: Session = Depends(deps.get_db), loan_id: int, loan_in: LoanUpdate
) -> Any:
    """
    Update a loan.
    """
    loan = crud.loan.get(db, id=loan_id)
    if not loan:
        raise HTTPException(
            status_code=404,
            detail="The loan with this ID does not exist in the system",
        )
    loan = crud.loan.update(db, db_obj=loan, obj_in=loan_in)
    return loan


@router.put("/{loan_id}/restructure", response_model=schemas.Loan)
def restructure_loan(
    *, db: Session = Depends(deps.get_db), loan_id: int, loan_in: LoanUpdate
) -> Any:
    """
    restructure a loan.
    """
    loan = crud.loan.get(db, id=loan_id)
    if not loan:
        raise HTTPException(
            status_code=404,
            detail="The loan with this ID does not exist in the system",
        )
    loan = crud.loan.restructure(db, db_obj=loan, obj_in=loan_in)
    return loan
