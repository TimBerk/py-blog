from _datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from settings.database import Base


class Post(Base):
    from models.user import User
    from models.tag import posts_tags_table
    from models.category import posts_categories_table

    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(40), nullable=False)
    text = Column(Text, nullable=False)
    is_published = Column(Boolean, nullable=False, default=False)
    published_by = Column(Integer, ForeignKey(User.id, onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    published_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', lazy="joined", back_populates='posts')
    tags = relationship('Tag', lazy="joined", secondary=posts_tags_table, back_populates='posts')
    categories = relationship('Category', lazy="joined", secondary=posts_categories_table, back_populates='posts')

    def __repr__(self):
        return f'<Post #{self.id} {self.title}>'
