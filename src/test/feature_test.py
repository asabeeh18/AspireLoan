import unittest
from fastapi.testclient import TestClient
from starlette import status

from src.main import app
from src.model import db_model
from src.model.request_model import LoanModel


def login(cls) -> None:
    payload = {'email': 'ahmed@gmaill.com', 'password': 'asd'}
    resp = cls.client.get("/user/login/", params=payload)
    return resp.json()


class MyTestCase(unittest.TestCase):
    client = TestClient(app)

    @classmethod
    def setUpClass(cls) -> None:
        db_model.initialize_db()

        #Login user
        payload = {'email': 'user@example.com', 'password': 'testpass'}
        resp = cls.client.get("/user/login/", params=payload)
        cls.user_token = resp.json()

    def test_01_new_user(self):
        payload = {"name": "test", "email": "user@example.com", "password": "testpass"}
        exp_resp = {
            "name": "test",
            "email": "user@example.com"
        }
        resp = self.client.post("/user/create/", json=payload)
        self.assertDictEqual(resp.json(),exp_resp)  # add assertion here

    def test_02_get_user(self):
        exp_resp = {
            "name": "test",
            "email": "user@example.com"
        }
        payload = {"id": 1}
        resp = self.client.get("/user/get/", params=payload)
        self.assertDictEqual(resp.json(),exp_resp) # add assertion here

    def test_03_login(self):
        payload = {'email': 'user@example.com', 'password': 'testpass'}
        resp = self.client.get("/user/login/", params=payload)
        self.assertEqual(resp.status_code,status.HTTP_200_OK)  # add assertion here

    def test_06_repay_loan(self):
        payload = {"loan_id": '1'}
        resp = self.client.get("/user/repay_loan", params=payload)
        self.assertEqual(True, False)  # add assertion here

    def test_04_new_loan(self):
        expected={'amount': 10.0, 'term': 2, 'start_date': '2023-08-28', 'user_token': self.user_token, 'loan_id': 1}
        new_loan = LoanModel(amount=10, term=2, start_date="2023-08-28", user_token=self.user_token)
        payload = new_loan.model_dump(mode="json")
        # payload = {"name": "test", "email": "user@example.com", "password": "testpass"}
        resp = self.client.post("/user/new_loan", json=payload)
        self.assertDictEqual(resp.json(), expected)  # add assertion here

    def test_05_get_repay_scehdule(self):
        exp={'schedule': [{'date': '2023-09-04', 'payment': 5.0, 'state': 'PENDING', 'loan_id': 1}, {'date': '2023-09-11', 'payment': 5.0, 'state': 'PENDING', 'loan_id': 1}]}
        payload = {"loan_id": "1", "user_token": self.user_token}
        resp = self.client.get("/user/repay_scehdule", params=payload)
        self.assertDictEqual(resp.json(), exp)  # add assertion here

if __name__ == "__main__":
    unittest.main()
    import os

    os.remove("AspireLoan.db")
