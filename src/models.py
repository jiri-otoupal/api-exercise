from sqlalchemy import String, Column, DateTime, Integer

from src.database import engine, Base


class Car(Base):
    __tablename__ = "car"

    cid = Column(Integer, primary_key=True)
    make = Column(String(255), nullable=False)
    model = Column(String(255), nullable=False)
    reserved_since = Column(DateTime, nullable=True, default=None)
    reserved_minutes = Column(Integer, nullable=True, default=None)


def init():
    Base.metadata.create_all(engine)


init()
