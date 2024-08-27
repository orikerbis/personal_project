import unittest
from app import app

class BasicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def test_add(self):
        response = self.client.get('/add/2/3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"result": 5})

        response = self.client.get('/add/10/20')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"result": 30})

if __name__ == "__main__":
    unittest.main()
