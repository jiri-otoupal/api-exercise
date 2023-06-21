import re

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src import crud
from src.database import get_db
from src.schemas import CarInput, CarDetailsInput, CarReservationInput
from src.utils import do_check

router = APIRouter()


@router.put("/add/")
async def add_car(car_details: CarInput, db: Session = Depends(get_db)):
    """

    @param car_details: Car Details
    @param db: Database session
    @return:
    """
    if not (match := re.match(r"^C(\d+)$", car_details.uid)):
        return JSONResponse(
            {"detail": "UID of car is in invalid format. Proper format 'C<number>'"},
            status_code=400)
    cid = match.group(1)

    try:
        crud.add_car(db=db, cid=cid, car=car_details)

    except IntegrityError:
        return JSONResponse({"detail": "Car with this UID exists"}, status_code=409)
    except Exception as ex:
        return JSONResponse({"detail": "Failed to add car", "exception": str(ex)},
                            status_code=400)

    return JSONResponse({"detail": "Successfully added car"}, status_code=200)


@router.delete("/rm/{car_uid}")
async def rm_car(car_uid, db: Session = Depends(get_db)):
    """

    @param car_uid: Unique Identifier of Car for deletion
    @param db: Database session
    @return:
    """
    if not (match := re.match(r"^C(\d+)$", car_uid)):
        return JSONResponse({
            "detail": "UID of car is in invalid format. Proper format 'C<number>'"},
            status_code=400)
    cid = match.group(1)
    c = crud.rm_car(db=db, cid=cid)
    if c is None:
        return JSONResponse({"detail": f"Car {car_uid} does not exist"},
                            status_code=400)
    return JSONResponse({"detail": "Successfully removed car"}, status_code=200)


@router.post("/update/{uid}")
async def update_car(uid: str, car_details: CarDetailsInput,
                     db: Session = Depends(get_db)):
    """

    @param uid: Unique Identifier of Car for update
    @param car_details: Details that will be changed
    @param db: Database session
    @return:
    """
    if not (match := re.match(r"^C(\d+)$", uid)):
        return JSONResponse(
            {"detail": "UID of car is in invalid format. Proper format 'C<number>'"},
            status_code=400)
    cid = match.group(1)

    c = crud.update_car(db=db, cid=cid, car=car_details)
    if c is None:
        return JSONResponse({"detail": f"Car {uid} does not exist"}, status_code=400)

    return JSONResponse({"detail": "Successfully updated car"}, status_code=200)


@router.get("/list")
async def get_cars(db: Session = Depends(get_db)):
    """
    Get All Cars
    @param db: Database session
    @return:
    """
    car_list = crud.get_cars(db)

    return JSONResponse({"cars": car_list})


@router.post("/reserve/{uid}")
async def reserve_car(uid: str, rsv_info: CarReservationInput,
                      db: Session = Depends(get_db)):
    """
    Reserve Specific Car
    @param uid: UID of car Example C123
    @param rsv_info: Reservation info
    @param db: Database session
    @return:
    """
    if not (match := re.match(r"^C(\d+)$", uid)):
        return JSONResponse(
            {"detail": "UID of car is in invalid format. Proper format 'C<number>'"},
            status_code=400)
    cid = match.group(1)

    car = crud.get_car(db=db, cid=cid)

    check = do_check(car, f"C{car.cid}", rsv_info)
    if check.status_code != 200:
        return check

    crud.reserve_car(db=db, cid=cid, car_rsv=rsv_info)
    return JSONResponse({"detail": "Successfully reserved car"}, status_code=200)


@router.post("/reserve/")
async def reserve_car_rand(rsv_info: CarReservationInput,
                           db: Session = Depends(get_db)):
    """
    Random Car Reservation
    @param rsv_info:  Info
    @param db: Database Session
    @return:
    """
    car = crud.get_free_car(db=db)

    if car is None:
        return JSONResponse({"detail": "No Cars available for reservation"},
                            status_code=400)

    check = do_check(car, f"C{car.cid}", rsv_info)
    if check.status_code != 200:
        return check

    crud.reserve_car(db=db, cid=car.cid, car_rsv=rsv_info)
    return JSONResponse(
        {"detail": f"Successfully reserved car C{car.cid} {car.make} {car.model}"},
        status_code=200)
