import datetime
import unittest

from starlette.testclient import TestClient

from main import app
from src.database import get_db, Base
from tests.test_base_function import override_get_db, engine

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


class BaseCallsCase(unittest.TestCase):
    def setUp(self) -> None:
        clean_db()

    def test_root(self):
        response = client.get("/")
        self.assertEqual(200, response.status_code)
        self.assertEqual({"msg": "Welcome to Car Reservation System!"}, response.json())

    def test_add_invalid_format(self):
        response = client.put("/car/add",
                              json={"make": "Toyota", "model": "ABC", "uid": "123"})
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            {"detail": "UID of car is in invalid format. Proper format 'C<number>'"},
            response.json())

    def test_add_duplicate(self):
        response = client.put("/car/add",
                              json={"make": "Toyota", "model": "ABC", "uid": "C123"})
        self.assertEqual(200, response.status_code)
        self.assertEqual({"detail": "Successfully added car"}, response.json())
        response = client.put("/car/add",
                              json={"make": "Toyota", "model": "ABC", "uid": "C123"})
        self.assertEqual(409, response.status_code)
        self.assertEqual({"detail": "Car with this UID exists"}, response.json())

    def test_update(self):
        response = client.post("/car/update/C222",
                               json={"make": "Toyoda"})
        self.assertEqual(400, response.status_code)
        self.assertEqual({"detail": f"Car C222 does not exist"}, response.json())

    def test_rm(self):
        response = client.delete("/car/rm/C123")
        self.assertEqual(response.status_code, 400)
        self.assertEqual({"detail": f"Car C123 does not exist"}, response.json())

    def test_reserve_too_ahead(self):
        self.populate_db_car()
        response = client.post("/car/reserve/C124",
                               json={"when": (
                                       datetime.datetime.now() + datetime.timedelta(
                                   days=10)).isoformat("-"),
                                     "duration": 10})
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            {"detail": "Reservations must be made no more than 24 hours in advance."},
            response.json())

    def test_reserve_too_late(self):
        self.populate_db_car()
        response = client.post("/car/reserve/C124",
                               json={"when": (
                                   datetime.datetime.now()).isoformat("-"),
                                     "duration": 10})
        self.assertEqual(400, response.status_code)
        self.assertEqual({"detail": "Reservations can not be made into history"},
                         response.json())

    def test_reserve_duration_too_big(self):
        self.populate_db_car()
        response = client.post("/car/reserve/C124",
                               json={"when": (
                                       datetime.datetime.now() + datetime.timedelta(
                                   minutes=86)).isoformat(
                                   "-"),
                                   "duration": 60 * 3})
        self.assertEqual(400, response.status_code)
        self.assertEqual({"detail": "Reservation duration too long, maximum is 2 hours"},
                         response.json())

    def test_reserve_duration_too_small(self):
        self.populate_db_car()
        response = client.post("/car/reserve/C124",
                               json={"when": (
                                       datetime.datetime.now() + datetime.timedelta(
                                   minutes=86)).isoformat(
                                   "-"),
                                   "duration": 0})
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            {"detail": "Reservation duration too short, minimum is 1 minute"},
            response.json())

    def test_rand_reserve_double(self):
        self.populate_db_car()
        response = client.post("/car/reserve/",
                               json={"when": (
                                       datetime.datetime.now() + datetime.timedelta(
                                   minutes=86)).isoformat(
                                   "-"),
                                   "duration": 10})
        self.assertEqual(200, response.status_code)
        self.assertEqual({"detail": "Successfully reserved car C124 Toyota ABC"},
                         response.json())
        response = client.post("/car/reserve/",
                               json={"when": (
                                       datetime.datetime.now() + datetime.timedelta(
                                   minutes=86)).isoformat(
                                   "-"),
                                   "duration": 10})
        self.assertEqual(400, response.status_code)
        self.assertEqual({"detail": "No Cars available for reservation"}, response.json())

    def populate_db_car(self):
        response = client.put("/car/add",
                              json={"make": "Toyota", "model": "ABC", "uid": "C124"})
        self.assertEqual(200, response.status_code)
        self.assertEqual({"detail": "Successfully added car"}, response.json())


if __name__ == '__main__':
    unittest.main()
