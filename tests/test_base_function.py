import datetime
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from main import app
from src.config import test_db_path
from src.database import get_db, Base

SQLALCHEMY_DATABASE_URL = f"sqlite:///{test_db_path}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


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

    def test_add(self):
        response = client.put("/car/add",
                              json={"make": "Toyota", "model": "ABC", "uid": "C123"})
        self.assertEqual(200, response.status_code)
        self.assertEqual({"detail": "Successfully added car"}, response.json())

    def test_update(self):
        response = client.put("/car/add",
                              json={"make": "Toyota", "model": "AXY", "uid": "C222"})
        self.assertEqual(200, response.status_code)

        response = client.post("/car/update/C222",
                               json={"make": "Toyoda"})
        self.assertEqual(200, response.status_code)
        self.assertEqual({"detail": "Successfully updated car"}, response.json())

    def test_rm(self):
        response = client.put("/car/add",
                              json={"make": "Toyota", "model": "ABC", "uid": "C123"})
        self.assertEqual(response.status_code, 200)
        response = client.delete("/car/rm/C123")
        self.assertEqual(response.status_code, 200)
        self.assertEqual({"detail": "Successfully removed car"}, response.json())

    def test_list(self):
        response = client.put("/car/add",
                              json={"make": "Toyota", "model": "ABC", "uid": "C124"})
        self.assertEqual(200, response.status_code)
        self.assertEqual({"detail": "Successfully added car"}, response.json())

        response = client.get("/car/list")
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {"cars": [{"uid": "C124", "make": "Toyota",
                       "model": "ABC",
                       "reserved_minutes": None,
                       "reserved_since": 'None'
                       }]
             }, response.json())

    def test_reserve(self):
        response = client.put("/car/add",
                              json={"make": "Toyota", "model": "ABC", "uid": "C124"})
        self.assertEqual(200, response.status_code)
        self.assertEqual({"detail": "Successfully added car"}, response.json())
        response = client.post("/car/reserve/C124",
                               json={"when": (
                                       datetime.datetime.now() + datetime.timedelta(
                                   minutes=86)).isoformat(
                                   "-"),
                                   "duration": 10})
        self.assertEqual(200, response.status_code)
        self.assertEqual({"detail": "Successfully reserved car"}, response.json())

    def test_rand_reserve_simple(self):
        response = client.put("/car/add",
                              json={"make": "Toyota", "model": "ABC", "uid": "C124"})
        self.assertEqual(200, response.status_code)
        self.assertEqual({"detail": "Successfully added car"}, response.json())
        response = client.post("/car/reserve/",
                               json={"when": (
                                       datetime.datetime.now() + datetime.timedelta(
                                   minutes=86)).isoformat(
                                   "-"),
                                   "duration": 10})
        self.assertEqual(200, response.status_code)
        self.assertEqual({"detail": "Successfully reserved car C124 Toyota ABC"},
                         response.json())

    def test_rand_reserve_adv(self):
        response = client.put("/car/add",
                              json={"make": "Toyota", "model": "ABC", "uid": "C124"})
        self.assertEqual(200, response.status_code)
        self.assertEqual({"detail": "Successfully added car"}, response.json())

        response = client.put("/car/add",
                              json={"make": "Toyota", "model": "AAX", "uid": "C125"})
        self.assertEqual(200, response.status_code)
        self.assertEqual({"detail": "Successfully added car"}, response.json())
        response = client.post("/car/reserve/",
                               json={"when": (
                                       datetime.datetime.now() + datetime.timedelta(
                                   minutes=86)).isoformat(
                                   "-"),
                                   "duration": 10})
        self.assertEqual(200, response.status_code)
        response = client.post("/car/reserve/",
                               json={"when": (
                                       datetime.datetime.now() + datetime.timedelta(
                                   minutes=86)).isoformat(
                                   "-"),
                                   "duration": 10})
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
