from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.services.item_service import ItemService
from app.core.decorators import measure_time

router = APIRouter(prefix="/items", tags=["Items"])


@router.post(
    "/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED
)
@measure_time
async def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db)
):
    return ItemService.create_item(db, item)


@router.get(
    "/",
    response_model=list[ItemResponse]
)
@measure_time
async def list_items(
    db: Session = Depends(get_db)
):
    return ItemService.list_items(db)


@router.patch(
    "/{item_id}",
    response_model=ItemResponse
)
@measure_time
async def update_item(
    item_id: int,
    item: ItemUpdate,
    db: Session = Depends(get_db)
):
    return ItemService.update_item(db, item_id, item)
