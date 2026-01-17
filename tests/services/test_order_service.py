from app.services.order_service import OrderService
from app.schemas.order import OrderCreate, OrderItemCreate
from app.models.category import Category
from app.models.item import Item
import pytest
from app.utils.exceptions import BadRequestException


def test_create_order_success(db_session):
    category = Category(name="Tools")
    db_session.add(category)
    db_session.commit()

    item = Item(
        name="Hammer",
        sku="HAM123",
        price=10,
        stock=5,
        category_id=category.id,
    )
    db_session.add(item)
    db_session.commit()

    order_data = OrderCreate(
        report_text="Fixing door",
        image_url=None,
        items=[
            OrderItemCreate(
                item_id=item.id,
                quantity=2
            )
        ]
    )

    order = OrderService.create_order(
        db=db_session,
        data=order_data,
        request_id="req-123"
    )

    assert order.id is not None
    assert len(order.items) == 1
    assert order.items[0].quantity == 2


def test_create_order_updates_stock(db_session):
    category = Category(name="Tools")
    db_session.add(category)
    db_session.commit()

    item = Item(
        name="Drill",
        sku="DRL123",
        price=100,
        stock=10,
        category_id=category.id,
    )
    db_session.add(item)
    db_session.commit()

    order_data = OrderCreate(
        report_text="Maintenance",
        image_url=None,
        items=[
            OrderItemCreate(item_id=item.id, quantity=3)
        ]
    )

    OrderService.create_order(
        db=db_session,
        data=order_data,
        request_id="req-456"
    )

    db_session.refresh(item)
    assert item.stock == 7


def test_create_order_insufficient_stock(db_session):
    category = Category(name="Tools")
    db_session.add(category)
    db_session.commit()

    item = Item(
        name="Saw",
        sku="SAW123",
        price=50,
        stock=1,
        category_id=category.id,
    )
    db_session.add(item)
    db_session.commit()

    order_data = OrderCreate(
        report_text="Repair",
        image_url=None,
        items=[
            OrderItemCreate(item_id=item.id, quantity=5)
        ]
    )

    with pytest.raises(BadRequestException):
        OrderService.create_order(
            db=db_session,
            data=order_data,
            request_id="req-789"
        )


def test_create_order_idempotency(db_session):
    category = Category(name="Tools")
    db_session.add(category)
    db_session.commit()

    item = Item(
        name="Wrench",
        sku="WRN123",
        price=20,
        stock=10,
        category_id=category.id,
    )
    db_session.add(item)
    db_session.commit()

    order_data = OrderCreate(
        report_text="Maintenance",
        image_url=None,
        items=[
            OrderItemCreate(item_id=item.id, quantity=1)
        ]
    )

    order1 = OrderService.create_order(
        db=db_session,
        data=order_data,
        request_id="req-999"
    )

    order2 = OrderService.create_order(
        db=db_session,
        data=order_data,
        request_id="req-999"
    )

    assert order1.id == order2.id
