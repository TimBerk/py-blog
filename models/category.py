from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from settings.database import Base


posts_categories_table = Table(
    'categories_posts',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id', onupdate="CASCADE", ondelete="CASCADE"),
           primary_key=True),
)


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(15), nullable=False)

    posts = relationship('Post', lazy="joined", secondary=posts_categories_table, back_populates='categories')

    def __repr__(self):
        return f'<Category #{self.id} {self.name}>'
