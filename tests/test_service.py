import json
import pytest
import requests

with open('./config/app.json') as f:
    config = json.load(f)

def test_default_prediction():
    """
    Test for the /default endpoint with valid input data.
    It should return a prediction in the response.
    """
    response = requests.post(f"http://localhost:{config["service_port"]}/default", json={
        'LIMIT_BAL': 0,
        'SEX': 1,
        'EDUCATION': 0,
        'MARRIAGE': 0,
        'AGE': 35,
        'PAY_0': 0,
        'PAY_2': 0,
        'PAY_3': 0,
        'PAY_4': 0,
        'PAY_5': 0,
        'PAY_6': 0,
        'BILL_AMT1': 0,
        'BILL_AMT2': 0,
        'BILL_AMT3': 0,
        'BILL_AMT4': 0,
        'BILL_AMT5': 0,
        'BILL_AMT6': 0,
        'PAY_AMT1': 0,
        'PAY_AMT2': 0,
        'PAY_AMT3': 0,
        'PAY_AMT4': 0,
        'PAY_AMT5': 0,
        'PAY_AMT6': 0
    })
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert isinstance(response.json()["prediction"], (int, float))
    assert response.json()["prediction"] == 0