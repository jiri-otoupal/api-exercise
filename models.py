from sqlalchemy import String, Column, DateTime, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Car(Base):
    __tablename__ = "car"

    cid = Column(Integer, primary_key=True)
    make = Column(String(255), nullable=False)
    model = Column(String(255), nullable=False)
    reserved_since = Column(DateTime, nullable=True, default=None)
    reserved_minutes = Column(Integer, nullable=True, default=None)


if __name__ == "__main__":
    from config import engine

    Base.metadata.create_all(engine)
