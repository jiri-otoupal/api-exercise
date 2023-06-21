from sqlalchemy.orm import Session

from .models import Car
from .schemas import CarInput, CarDetailsInput


def get_cars(db: Session) -> list:
    cars_raw = db.query(Car).all()

    car_list = [dict(filter(lambda x: not x[0].startswith("_"), car.__dict__.items()))
                for car
                in cars_raw]

    for car in car_list:
        car["uid"] = f'C{car.pop("cid")}'
        car["reserved_since"] = str(car["reserved_since"])
    return car_list


def add_car(db: Session, cid, car: CarInput):
    car = Car(cid=cid, make=car.make, model=car.model)
    db.add(car)
    db.commit()
    return car


def rm_car(db: Session, cid: int):
    c = db.get(Car, cid)
    if c is None:
        return c

    db.delete(c)
    db.commit()
    return c


def update_car(db: Session, cid: int, car: CarDetailsInput):
    c = db.get(Car, cid)
    if c is None:
        return c

    for key, value in dict(car).items():
        if value is not None:
            setattr(c, key, value)
    db.commit()
    return c
