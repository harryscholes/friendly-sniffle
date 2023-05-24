from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

wallet_address = "0x6105f0b07341eE41562fd359Ff705a8698Dd3109"


def test_get_tokens_for_address():
    response = client.get(f"/get-tokens-for-address/address/{wallet_address}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["tokens"]) > 0


def test_get_usd_value_for_address():
    response = client.get(f"/get-usd-value-for-address/address/{wallet_address}")
    assert response.status_code == 200
    data = response.json()
    assert data["usd_value"] > 0.0


def test_get_transactions_for_address():
    response = client.get(f"/get-transactions-for-address/address/{wallet_address}/page/0")
    assert response.status_code == 200
    data = response.json()
    assert len(data["transactions"]) > 0

    response = client.get(f"/get-transactions-for-address/address/{wallet_address}/page/1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["transactions"]) > 0
