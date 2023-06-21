from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from .models import Car
from .schemas import CarInput, CarDetailsInput, CarReservationInput


def get_car(db: Session, cid: int):
    return db.get(Car, cid)


def get_cars(db: Session) -> list:
    cars_raw = db.query(Car).all()

    car_list = [dict(filter(lambda x: not x[0].startswith("_"), car.__dict__.items()))
                for car
                in cars_raw]

    for car in car_list:
        car["uid"] = f'C{car.pop("cid")}'
        car["reserved_since"] = str(car["reserved_since"])
    return car_list


def add_car(db: Session, cid: int, car: CarInput):
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


def reserve_car(db: Session, cid: int, car_rsv: CarReservationInput):
    car = db.get(Car, cid)
    car.reserved_since = datetime.fromisoformat(car_rsv.when)
    car.reserved_minutes = car_rsv.duration

    db.commit()
    return car


def get_free_car(db: Session):
    car = db.query(Car).where(
        (Car.reserved_since == None) | (
                Car.reserved_since > (
                datetime.now() + timedelta(hours=24)))).first()  # noqa
    return car
