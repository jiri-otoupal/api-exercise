import re

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from main import app
from src.config import engine
from src.models import Car
from src.req_inputs import CarInput, CarDetailsInput


@app.put("/addcar/")
async def add_car(car: CarInput):
    if not (match := re.match(r"^C(\d+)$", car.uid)):
        return JSONResponse({"detail": "UID of car is in invalid format. Proper format 'C<number>'"})
    cid = match.group(1)

    try:
        with Session(engine) as session:
            car = Car(cid=cid, make=car.make, model=car.model)
            session.add(car)
            session.commit()

    except IntegrityError:
        return JSONResponse({"detail": "Car with this UID exists"}, status_code=409)
    except Exception as ex:
        return JSONResponse({"detail": "Failed to add car", "exception": str(ex)}, status_code=400)

    return JSONResponse({"detail": "Successfully added car"}, status_code=200)


@app.delete("/rmcars/{car_uid}")
async def rm_car(car_uid):
    try:
        with Session(engine) as session:
            if not (match := re.match(r"^C(\d+)$", car_uid)):
                return JSONResponse({"detail": "UID of car is in invalid format. Proper format 'C<number>'"})
            cid = match.group(1)

            c = session.query(Car).get(cid)
            if c is None:
                return JSONResponse({"detail": f"Car {car_uid} does not exist"})

            session.delete(c)
            session.commit()

            return JSONResponse({"detail", "Successfully removed car"}, status_code=200)
    except IntegrityError:
        return JSONResponse({"detail": "Car with this UID exists"}, status_code=400)


@app.post("/update_car/{uid}")
def update_car(uid: str, car: CarDetailsInput):
    if not (match := re.match(r"^C(\d+)$", uid)):
        return JSONResponse({"detail": "UID of car is in invalid format. Proper format 'C<number>'"})
    cid = match.group(1)

    with Session(engine) as session:
        c = session.query(Car).get(cid)
        if c is None:
            return JSONResponse({"detail": f"Car {cid} does not exist"})

        for key, value in dict(car).items():
            setattr(c, key, value)

        session.commit()

    return JSONResponse({"detail": "Successfully updated car"}, status_code=200)


@app.get("/cars")
def get_cars():
    with Session(engine) as session:
        cars_raw = session.query(Car).all()

        car_list = [dict(filter(lambda x: "_" not in x[0], car.__dict__.items())) for car in cars_raw]

        return JSONResponse({"cars": car_list})

    # TODO: make reservation
    # TODO: list cars
