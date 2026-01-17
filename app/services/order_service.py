from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.idempotency import IdempotencyKey

from app.repositories.order_repository import OrderRepository
from app.repositories.item_repository import ItemRepository
from app.repositories.idempotency_repository import IdempotencyRepository


class OrderService:

    @staticmethod
    def create_order(
        db: Session,
        data,
        request_id: str
    ) -> Order:

        existing_key = IdempotencyRepository.get_by_request_id(db, request_id)

        if existing_key is not None:
            order = OrderRepository.get_by_id(db, int(existing_key.order_id))
            if order is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Order {existing_key.order_id} not found"
                )
            return order

        order = Order(
            report_text=data.report_text,
            image_url=data.image_url
        )

        order = OrderRepository.create(db, order)

        order_items = []

        for item_data in data.items:
            item = ItemRepository.get_by_id(db, item_data.item_id)

            if item is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Item {item_data.item_id} not found"
                )

            if item.stock < item_data.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for item {item.id}"
                )

            item.stock -= item_data.quantity

            order_items.append(
                OrderItem(
                    order_id=order.id,
                    item_id=item.id,
                    quantity=item_data.quantity,
                    unit_price=item.price
                )
            )

        OrderRepository.add_order_items(db, order_items)

        key = IdempotencyKey(
            request_id=request_id,
            order_id=order.id
        )

        IdempotencyRepository.create(db, key)

        return order
