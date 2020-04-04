from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

ENGINE = create_engine('sqlite:///blog.db')
METADATA = MetaData()
Base = declarative_base(ENGINE)

session_factory = sessionmaker(bind=ENGINE)
Session = scoped_session(session_factory)
