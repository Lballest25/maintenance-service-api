from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.decorators import measure_time
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import OrderService
from app.utils.exceptions import BadRequestException

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED
)
@measure_time
async def create_order(
    order: OrderCreate,
    request_id: str = Header(..., alias="X-Request-ID"),
    db: Session = Depends(get_db),
):
    """
    Create a new order.
    :param order: Order data
    :param request_id: Unique request identifier from headers
    :param db: Database session
    :return: Created Order object
    """
    if request_id is None:
        raise BadRequestException("X-Request-ID header is required")

    return OrderService.create_order(db, order, request_id)
