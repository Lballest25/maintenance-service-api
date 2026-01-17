from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.item import Item


class ItemRepository:

    @staticmethod
    def create(db: Session, item: Item) -> Item:
        try:
            db.add(item)
            db.commit()
            db.refresh(item)
            return item
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @staticmethod
    def get_all(db: Session):
        return db.query(Item).all()

    @staticmethod
    def get_by_id(db: Session, item_id: int) -> Item | None:
        return db.query(Item).filter(Item.id == item_id).first()

    @staticmethod
    def get_by_sku(db: Session, sku: str) -> Item | None:
        return db.query(Item).filter(Item.sku == sku).first()

    @staticmethod
    def update(db: Session, item: Item) -> Item:
        try:
            db.commit()
            db.refresh(item)
            return item
        except SQLAlchemyError as e:
            db.rollback()
            raise e
