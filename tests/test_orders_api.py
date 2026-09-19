from utils.api_client import APIClient
from app.database import get_connection


client = APIClient()


def test_create_order_and_verify_database():
    product_response = client.post(
        "/products",
        {
            "name": "QA Monitor",
            "price": 15000,
            "stock": 5
        }
    )

    assert product_response.status_code == 201

    product_id = product_response.json()["id"]

    response = client.post(
        "/orders",
        {
            "product_id": product_id,
            "quantity": 2
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["product_id"] == product_id
    assert data["quantity"] == 2
    assert data["total"] == 30000

    connection = get_connection()

    order = connection.execute(
        "SELECT * FROM orders WHERE id = ?",
        (data["id"],)
    ).fetchone()

    connection.close()

    assert order is not None
    assert order["product_id"] == product_id
    assert order["quantity"] == 2
    assert order["total"] == 30000


def test_create_order_with_invalid_product():
    response = client.post(
        "/orders",
        {
            "product_id": 999999,
            "quantity": 1
        }
    )

    assert response.status_code == 404