import unittest

from starlette.testclient import TestClient

from main import app

client = TestClient(app)


class BaseCallsCase(unittest.TestCase):

    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"msg": "Welcome to Car Reservation System!"}


if __name__ == '__main__':
    unittest.main()
