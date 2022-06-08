from .crud_user import user
from .crud_fine import fine
from .crud_saving import saving
from .crud_loan import loan
from .crud_instalment import instalment


# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
