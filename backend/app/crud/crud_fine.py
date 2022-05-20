from typing import Any, Dict, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.fine import Fine
from app.schemas.fine import FineCreate, FineUpdate


class CRUDFine(CRUDBase[Fine, FineCreate, FineUpdate]):
    def get_by_id(self, db: Session, *, id: int) -> None | Fine:
        return db.query(Fine).filter(Fine.id == id).first()

    def create(self, db: Session, *, obj_in: FineCreate) -> Fine:
        db_obj = Fine(
            amount=obj_in.amount,
            reason=obj_in.reason,
            paid=obj_in.paid,
            member_id=obj_in.member_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Fine, obj_in: Union[FineUpdate, Dict[str, Any]]
    ) -> Fine:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


fine = CRUDFine(Fine)
