import pytest
from fastapi.testclient import  TestClient

from bootstrap import get_db
from main import app
from . import get_test_db
from .conftest import t_client



def test_get_categories(t_client):


    response = t_client.get(
        "/categories",
        headers={
            "Accept": "application/json",
        },
    )



def test_create_category(t_client):

    payload = {
        "name": "pytest_create"
    }

    response = t_client.post(
        "/categories",
        json=payload,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mzg2MTYyMDYsInN1YiI6Im11amFkaWQifQ.nlaI3GTkQ82gRXJYQbkJtEFZPWCx4WUdWiIxGzTolFk"
        }
    )

    print("Response Status Code:", response.status_code)
    print("Response Body:", response.json())

    assert response.status_code in [200, 201]  # Expect 200 or 201 for creation success
    data = response.json()

    assert "data" in data, "Response JSON should contain 'data'"
    assert "name" in data["data"], "Response JSON 'data' should contain 'name'"
    assert data["data"]["name"] == "pytest_create", f"Expected 'pytest_create', got {data['data']['name']}"
    assert data.get("success") is True, "Response should indicate success"

