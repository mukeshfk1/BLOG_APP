from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker


engine = create_engine("sqlite:///blog_db.db")


base = declarative_base()


def create_session():
    ses = sessionmaker(engine)

    return ses()


def create_tables():
    base.metadata.create_all(engine)