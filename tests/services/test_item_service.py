import pytest
from app.services.item_service import ItemService
from app.schemas.item import ItemCreate
from app.models.category import Category
from app.utils.exceptions import NotFoundException


def test_create_item_with_invalid_category(db_session):
    """
    Test creating an item with a non-existent category.
    """
    item_data = ItemCreate(
        name="Test Item",
        sku="SKU123",
        price=10.0,
        stock=5,
        category_id=999,
    )

    with pytest.raises(NotFoundException):
        ItemService.create_item(db_session, item_data)


def test_create_item_success(db_session):
    """
    Test successful creation of an item with a valid category.
    """
    category = Category(name="Tools")
    db_session.add(category)
    db_session.commit()

    item_data = ItemCreate(
        name="Hammer",
        sku="HAM123",
        price=15.0,
        stock=10,
        category_id=category.id,
    )

    item = ItemService.create_item(db_session, item_data)

    assert item.id is not None
    assert item.category_id == category.id
