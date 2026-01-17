from app.models.item import Item
from app.repositories.item_repository import ItemRepository


def test_get_item_by_sku(db_session):
    """
    Test retrieving an item by its SKU.
    """
    item = Item(
        name="Mouse",
        sku="MOU123",
        price=20,
        stock=5,
        category_id=1,
    )

    db_session.add(item)
    db_session.commit()

    found = ItemRepository.get_by_sku(db_session, "MOU123")
    assert found is not None
    assert found.sku == "MOU123"
