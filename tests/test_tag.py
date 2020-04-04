import pytest
from sqlalchemy.sql import exists

from settings.database import Base, Session, ENGINE
from models import User, Tag
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


class TestTag:

    def test_create_and_delete_tag(self, session):
        new_tag = Tag(name='web')
        session.add(new_tag)
        session.commit()

        assert new_tag.id == 1

        delete_tag = session.query(Tag).filter(Tag.id == new_tag.id)
        delete_tag.delete()
        session.commit()

        check_tag = session.query(exists().where(Tag.id == new_tag.id)).scalar()
        assert check_tag is False
