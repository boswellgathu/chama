from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import dependencies as deps
from app import crud, schemas

router = APIRouter()


@router.get("/")
async def hello():
    return {"message": "hello Fines!"}


@router.post("/", response_model=schemas.Fine)
def create_fine(
    *, db: Session = Depends(deps.get_db), fine_in: schemas.FineCreate
) -> Any:
    """
    Create new fine.
    """
    fine = crud.fine.create(db, obj_in=fine_in)
    return fine


@router.put("/{fine_id}", response_model=schemas.Fine)
def update_fine(
    *, db: Session = Depends(deps.get_db), fine_id: int, fine_in: schemas.FineUpdate
) -> Any:
    """
    Update a fine.
    """

    fine = crud.fine.get(db, id=fine_id)
    if not fine:
        raise HTTPException(
            status_code=404,
            detail="The fine with this id does not exist in the system",
        )
    try:
        fine = crud.fine.update(db, db_obj=fine, obj_in=fine_in)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=str(err.args),
        )
    return fine
