from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from settings.database import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)

    posts = relationship('Post', back_populates='user', cascade="save-update, merge, delete")

    def __repr__(self):
        return f'<User #{self.id} {self.username}>'
