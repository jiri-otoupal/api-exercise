import re

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src import crud
from src.database import engine, get_db
from src.schemas import CarInput, CarDetailsInput
from src.models import Car

router = APIRouter()


@router.put("/add/")
async def add_car(car: CarInput, db: Session = Depends(get_db)):
    if not (match := re.match(r"^C(\d+)$", car.uid)):
        return JSONResponse(
            {"detail": "UID of car is in invalid format. Proper format 'C<number>'"})
    cid = match.group(1)

    try:
        crud.add_car(db=db, cid=cid, car=car)

    except IntegrityError:
        return JSONResponse({"detail": "Car with this UID exists"}, status_code=409)
    except Exception as ex:
        return JSONResponse({"detail": "Failed to add car", "exception": str(ex)},
                            status_code=400)

    return JSONResponse({"detail": "Successfully added car"}, status_code=200)


@router.delete("/rm/{car_uid}")
async def rm_car(car_uid, db: Session = Depends(get_db)):
    try:
        with Session(engine) as session:
            if not (match := re.match(r"^C(\d+)$", car_uid)):
                return JSONResponse({
                    "detail": "UID of car is in invalid format. Proper format 'C<number>'"})
            cid = match.group(1)

            c = crud.rm_car(db=db, cid=cid)
            if c is None:
                return JSONResponse({"detail": f"Car {car_uid} does not exist"})

            return JSONResponse({"detail": "Successfully removed car"}, status_code=200)
    except IntegrityError:
        return JSONResponse({"detail": "Car with this UID exists"}, status_code=400)


@router.post("/update/{uid}")
async def update_car(uid: str, car: CarDetailsInput, db: Session = Depends(get_db)):
    if not (match := re.match(r"^C(\d+)$", uid)):
        return JSONResponse(
            {"detail": "UID of car is in invalid format. Proper format 'C<number>'"})
    cid = match.group(1)

    c = crud.update_car(db=db, cid=cid, car=car)
    if c is None:
        return JSONResponse({"detail": f"Car {cid} does not exist"}, status_code=400)

    return JSONResponse({"detail": "Successfully updated car"}, status_code=200)


@router.get("/list")
async def get_cars(db: Session = Depends(get_db)):
    car_list = crud.get_cars(db)

    return JSONResponse({"cars": car_list})

    # TODO: make reservation
    # TODO: list cars
