from fastapi import status

from app.utils.exceptions import (
    NotFoundException,
    ConflictException,
    BadRequestException,
)


def test_not_found_exception_default_message():
    exc = NotFoundException()

    assert exc.status_code == status.HTTP_404_NOT_FOUND
    assert exc.detail == "Resource not found"


def test_not_found_exception_custom_message():
    exc = NotFoundException("Category not found")

    assert exc.status_code == status.HTTP_404_NOT_FOUND
    assert exc.detail == "Category not found"


def test_conflict_exception():
    exc = ConflictException("SKU already exists")

    assert exc.status_code == status.HTTP_409_CONFLICT
    assert exc.detail == "SKU already exists"


def test_bad_request_exception():
    exc = BadRequestException("Invalid payload")

    assert exc.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.detail == "Invalid payload"
