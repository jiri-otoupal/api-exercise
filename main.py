import re

from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from config import engine
from models import Car
from req_inputs import CarInput, CarDetailsInput

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to Car Reservation System!"}


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
            if value is not None:
                setattr(c, key, value)

        session.commit()

    return JSONResponse({"detail": "Successfully updated car"}, status_code=200)
