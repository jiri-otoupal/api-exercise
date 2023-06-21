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
        response = client.put("/car/add",
                              json={"make": "Toyota", "model": "ABC", "uid": "C123"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"detail": "Successfully added car"})

    def test_update(self):
        response = client.put("/car/add",
                              json={"make": "Toyota", "model": "AXY", "uid": "C222"})
        self.assertEqual(response.status_code, 200)

        response = client.post("/car/update/C222",
                               json={"make": "Toyoda"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"detail": "Successfully updated car"})

        response = client.delete("/car/rm/C222")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"detail": "Successfully removed car"})

    def test_rm(self):
        response = client.delete("/car/rm/C123")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"detail": "Successfully removed car"})

    def test_order(self):
        pass

    def test_list(self):
        pass


if __name__ == '__main__':
    unittest.main()
