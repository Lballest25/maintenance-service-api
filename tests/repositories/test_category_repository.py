from app.models.category import Category
from app.repositories.category_repository import CategoryRepository


def test_create_category(db_session):
    category = Category(name="Tools")

    created = CategoryRepository.create(db_session, category)

    assert created.id is not None
    assert created.name == "Tools"


def test_get_category_by_id(db_session):
    category = Category(name="Hardware")
    db_session.add(category)
    db_session.commit()

    found = CategoryRepository.get_by_id(db_session, category.id)

    assert found is not None
    assert found.name == "Hardware"


def test_get_all_categories(db_session):
    db_session.add_all(
        [Category(name="A"), Category(name="B")]
    )
    db_session.commit()

    categories = CategoryRepository.get_all(db_session)

    assert len(categories) == 2
