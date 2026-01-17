from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Numeric,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)

    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    item = relationship("Item")

    __table_args__ = (
        UniqueConstraint("order_id", "item_id", name="uq_order_item"),
    )
