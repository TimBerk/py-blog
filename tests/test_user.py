import pytest
from sqlalchemy.sql import exists

from settings.database import Base, Session, ENGINE
from models import User
from tests.const import USER_1


@pytest.fixture(scope="function")
def session():
    session = Session()
    yield session
    session.close()


def reset_db():
    Base.metadata.drop_all(bind=ENGINE)
    Base.metadata.create_all()


def create_user(session):
    user = User(username=USER_1)
    session.add(user)
    session.commit()
    return user


class TestUser:

    def test_create_user(self, session):
        reset_db()
        new_user = create_user(session)
        assert new_user.id == 1

    def test_delete_user(self, session):
        new_user = create_user(session)

        delete_user = session.query(User).filter(User.id == new_user.id)
        delete_user.delete()
        session.commit()

        check_user = session.query(exists().where(User.id == new_user.id)).scalar()

        assert check_user is False
