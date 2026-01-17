from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.utils.exceptions import ConflictException, NotFoundException


class CategoryService:

    @staticmethod
    def list_categories(db: Session):
        return CategoryRepository.get_all(db)

    @staticmethod
    def create_category(db: Session, name: str):
        existing = CategoryRepository.get_by_name(db, name)
        if existing:
            raise ConflictException("Category already exists")

        category = Category(name=name)
        return CategoryRepository.create(db, category)

    @staticmethod
    def get_category(db: Session, category_id: int):
        category = CategoryRepository.get_by_id(db, category_id)
        if not category:
            raise NotFoundException("Category not found")

        return category
