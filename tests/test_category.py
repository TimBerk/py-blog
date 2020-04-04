import pytest

from settings.database import Base, Session, ENGINE
from models import User, Category
from tests.const import USER_1


@pytest.fixture(scope="function")
def session():
    session = Session()
    yield session
    session.close()


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=ENGINE)
    Base.metadata.create_all()


def create_user(session):
    user = User(username=USER_1)
    session.add(user)
    session.commit()
    return user


class TestCategory:

    def test_create_and_delete_category(self, session):
        new_category = Category(name='Book')
        new_category2 = Category(name='Book')
        session.add(new_category)
        session.add(new_category2)
        session.commit()

        assert new_category.id == 1

        delete_category = session.query(Category).filter(Category.id == new_category.id)
        delete_category.delete()
        session.commit()

        check_count_category = session.query(Category).count()
        assert check_count_category == 1
