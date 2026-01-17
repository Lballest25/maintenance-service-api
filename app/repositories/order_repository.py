from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem


class OrderRepository:

    @staticmethod
    def create(db: Session, order: Order) -> Order:
        try:
            db.add(order)
            db.commit()
            db.refresh(order)
            return order
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @staticmethod
    def add_order_items(db: Session, order_items: list[OrderItem]):
        try:
            db.add_all(order_items)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @staticmethod
    def get_by_id(db: Session, order_id: int) -> Order | None:
        return db.query(Order).filter(Order.id == order_id).first()
