import pytest
from sqlalchemy.sql import exists

from settings.database import Base, Session, ENGINE
from models import User, Post
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


class TestPost:

    def test_create_post_by_user(self, session):
        user = create_user(session)

        new_post = Post(
            published_by=user.id,
            title='Post 1',
            text='Checked creating new post by user',
            is_published=True)
        session.add(new_post)
        session.commit()
        assert new_post.id == 1

    def test_delete_post_by_user(self, session):
        user = create_user(session)
        post = Post(published_by=user.id, title='Post 2', text='Checked delete post by user', is_published=False)
        session.add(post)
        session.commit()

        delete_post = session.query(Post).filter(Post.id == post.id)
        delete_post.delete()
        session.commit()

        check_user = session.query(exists().where(Post.id == post.id)).scalar()

        assert check_user is False

    def test_several_posts_by_user(self, session):
        user1 = create_user(session)
        user2 = create_user(session)
        user3 = create_user(session)

        post1 = Post(
            published_by=user1.id,
            title='Продажам iPhone прогнозируют заметное снижение',
            text='Аналитики из компании Fubon Research прогнозируют падение продаж iPhone в первом квартале текущего'
                 'года на 17% с 41 млн штук до 35 млн шт.',
            is_published=False)
        post2 = Post(
            published_by=user2.id,
            title='ОС Аврора прошла данную проверку по профилю защиты для ОС «А» четвертого класса, что подтверждает'
                  'сертификат ФСТЭК 4220 от 10.02.2020',
            text='Мобильная ОС Аврора выходит на новый уровень доверия', is_published=True
        )
        post3 = Post(
            published_by=user2.id,
            title='Telegram vs SEC: токены Gram признаны ценными бумагами',
            text='По данным SEC, было продано около 2,9 млрд токенов Gram, около 1 млрд которых приобретены'
                 'американскими инвесторами, сумма сделок - $425,5 млн. ',
            is_published=False
        )
        post4 = Post(
            published_by=user3.id,
            title='«Марвел» открыл онлайн ИТ-университет',
            text='MARVELous IT University включает расписание актуальных вебинаров, медиабиблиотеку презентаций и'
                 'видеозаписей, а также новостной раздел',
            is_published=True)
        session.add(post1)
        session.add(post2)
        session.add(post3)
        session.add(post4)
        session.commit()

        user2_post = session.query(Post.id).filter(Post.published_by == user2.id).count()
        assert user2_post == 2

        published_post = session.query(Post.id).filter(Post.is_published.is_(True)).count()
        assert published_post == 2

    def test_delete_user_with_posts(self, session):
        user1 = create_user(session)
        user2 = create_user(session)

        post1 = Post(
            published_by=user1.id,
            title='Продажам iPhone прогнозируют заметное снижение',
            text='Аналитики из компании Fubon Research прогнозируют падение продаж iPhone в первом квартале текущего'
                 'года на 17% с 41 млн штук до 35 млн шт.',
            is_published=False)
        post2 = Post(
            published_by=user2.id,
            title='ОС Аврора прошла данную проверку по профилю защиты для ОС «А» четвертого класса, что подтверждает'
                  'сертификат ФСТЭК 4220 от 10.02.2020',
            text='Мобильная ОС Аврора выходит на новый уровень доверия', is_published=True
        )
        post3 = Post(
            published_by=user2.id,
            title='Telegram vs SEC: токены Gram признаны ценными бумагами',
            text='По данным SEC, было продано около 2,9 млрд токенов Gram, около 1 млрд которых приобретены'
                 'американскими инвесторами, сумма сделок - $425,5 млн. ',
            is_published=False
        )
        session.add(post1)
        session.add(post2)
        session.add(post3)
        session.commit()

        delete_user = session.query(User).filter(User.id == user2.id).first()
        session.delete(delete_user)
        session.commit()

        check_user = session.query(exists().where(Post.published_by == user2.id)).scalar()
        assert check_user is False

        posts = session.query(Post.id).count()
        assert posts == 1
