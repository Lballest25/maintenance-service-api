from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.idempotency import IdempotencyKey


class IdempotencyRepository:

    @staticmethod
    def get_by_request_id(
        db: Session,
        request_id: str,
    ) -> IdempotencyKey | None:
        return (
            db.query(IdempotencyKey)
            .filter(IdempotencyKey.request_id == request_id)
            .first()
        )

    @staticmethod
    def create(db: Session, key: IdempotencyKey) -> IdempotencyKey:
        try:
            db.add(key)
            db.commit()
            db.refresh(key)
            return key
        except SQLAlchemyError as e:
            db.rollback()
            raise e
