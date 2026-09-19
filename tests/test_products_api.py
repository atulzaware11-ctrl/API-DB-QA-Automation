from utils.api_client import APIClient
from app.database import get_connection


client = APIClient()


def test_create_product_and_verify_database():
    payload = {
        "name": "QA Laptop",
        "price": 75000,
        "stock": 10
    }

    response = client.post("/products", payload)

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "QA Laptop"
    assert data["price"] == 75000
    assert data["stock"] == 10

    connection = get_connection()

    product = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (data["id"],)
    ).fetchone()

    connection.close()

    assert product is not None
    assert product["name"] == "QA Laptop"
    assert product["price"] == 75000
    assert product["stock"] == 10


def test_get_products():
    response = client.get("/products")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_non_existing_product():
    response = client.get("/products/999999")

    assert response.status_code == 404


def test_update_product():
    create_response = client.post(
        "/products",
        {
            "name": "Update Test Product",
            "price": 5000,
            "stock": 5
        }
    )

    assert create_response.status_code == 201

    product_id = create_response.json()["id"]

    response = client.put(
        f"/products/{product_id}",
        {
            "name": "Updated Product",
            "price": 6000,
            "stock": 10
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated Product"
    assert data["price"] == 6000
    assert data["stock"] == 10


def test_delete_product():
    create_response = client.post(
        "/products",
        {
            "name": "Delete Test Product",
            "price": 1000,
            "stock": 2
        }
    )

    assert create_response.status_code == 201

    product_id = create_response.json()["id"]

    response = client.delete(
        f"/products/{product_id}"
    )

    assert response.status_code == 200

    verify_response = client.get(
        f"/products/{product_id}"
    )

    assert verify_response.status_code == 404