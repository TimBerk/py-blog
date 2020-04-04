# flake8: noqa
from .post import Post
from .user import User
from .tag import Tag, posts_tags_table
from .category import Category, posts_categories_table

from settings.database import Base, ENGINE


def create_all_tables():
    Base.metadata.create_all()


def delete_all_tables():
    Base.metadata.drop_all(bind=ENGINE)
