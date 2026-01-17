from sqlalchemy.orm import Session

from app.models.item import Item
from app.repositories.category_repository import CategoryRepository
from app.repositories.item_repository import ItemRepository
from app.utils.exceptions import BadRequestException, NotFoundException


class ItemService:

    @staticmethod
    def create_item(db: Session, data) -> Item:
        """
        Create a new item after validating the input data.
        :param db: Database session
        :param data: Data for the new item
        :return: Created Item object
        """
        category = CategoryRepository.get_by_id(db, data.category_id)
        if category is None:
            raise NotFoundException("Category not found")

        existing_item = ItemRepository.get_by_sku(db, data.sku)

        if existing_item is not None:
            raise BadRequestException("Item with this SKU already exists")

        item = Item(
            name=data.name,
            sku=data.sku,
            price=data.price,
            stock=data.stock,
            category_id=data.category_id,
        )

        return ItemRepository.create(db, item)

    @staticmethod
    def list_items(db: Session):
        """
        Retrieve all items from the database.
        :param db: Database session
        :return: List of Item objects
        """
        return ItemRepository.get_all(db)

    @staticmethod
    def update_item(db: Session, item_id: int, data) -> Item:
        """
        Update an existing item with new data.
        :param db: Database session
        :param item_id: ID of the item to update
        :param data: New data for the item
        :return: Updated Item object
        """
        item = ItemRepository.get_by_id(db, item_id)

        if item is None:
            raise NotFoundException("Item not found")

        if data.price is not None:
            item.price = data.price

        if data.stock is not None:
            item.stock = data.stock

        return ItemRepository.update(db, item)
