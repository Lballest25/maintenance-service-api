import pytest

from app.services.category_service import CategoryService
from app.utils.exceptions import ConflictException


def test_create_category_success(db_session):
    category = CategoryService.create_category(db_session, "Electronics")

    assert category.id is not None
    assert category.name == "Electronics"


def test_create_category_duplicate(db_session):
    CategoryService.create_category(db_session, "Books")

    with pytest.raises(ConflictException):
        CategoryService.create_category(db_session, "Books")
