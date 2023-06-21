import unittest

from starlette.testclient import TestClient

from main import app

client = TestClient(app)


class BaseCallsCase(unittest.TestCase):

    def test_root(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"msg": "Welcome to Car Reservation System!"})

    def test_add(self):
        response = client.put("/addcar/",
                              json={"make": "Toyota", "model": "ABC", "uid": "C123"})
        self.assertEqual(response.status_code, 200)

    def test_rm(self):
        pass

    def test_update(self):
        pass

    def test_order(self):
        pass

    def test_list(self):
        pass


if __name__ == '__main__':
    unittest.main()
