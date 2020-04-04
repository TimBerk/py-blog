from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from settings.database import Base


posts_tags_table = Table(
    'tags_posts',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)

    posts = relationship('Post', secondary=posts_tags_table, back_populates='tags')

    def __repr__(self):
        return f'<Tag #{self.id} {self.name}>'
