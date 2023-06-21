import datetime

from starlette.responses import JSONResponse


def do_check(car, uid, rsv_info):
    if car is None:
        return JSONResponse({"detail": f"Car {uid} does not exist"}, status_code=400)

    if car.reserved_since is not None:

        if (
                datetime.datetime.now() - car.reserved_since).seconds < 24 * 60 * 60:
            return JSONResponse({"detail": f"Car {uid} is already reserved"},
                                status_code=400)

    if rsv_info.duration > 60 * 2:
        return JSONResponse(
            {"detail": "Reservation duration too long, maximum is 2 hours"},
            status_code=400)

    if rsv_info.duration < 1:
        return JSONResponse(
            {"detail": "Reservation duration too short, minimum is 1 minute"},
            status_code=400)

    if (datetime.datetime.fromisoformat(
            rsv_info.when) < datetime.datetime.now()):
        return JSONResponse(
            {"detail": "Reservations can not be made into history"},
            status_code=400)

    if (datetime.datetime.fromisoformat(
            rsv_info.when) - datetime.datetime.now()) > datetime.timedelta(hours=24):
        return JSONResponse(
            {"detail": "Reservations must be made no more than 24 hours in advance."},
            status_code=400)

    return JSONResponse({}, status_code=200)
