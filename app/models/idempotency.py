from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.core.database import Base


class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String(100), nullable=False, unique=True)

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
