from flask import Flask, jsonify, request
from app.database import get_connection, initialize_database

app = Flask(__name__)

initialize_database()


@app.get("/products")
def get_products():
    connection = get_connection()

    products = connection.execute(
        "SELECT * FROM products"
    ).fetchall()

    connection.close()

    return jsonify([dict(product) for product in products]), 200


@app.post("/products")
def create_product():
    data = request.get_json()

    if not data or not all(
        key in data for key in ["name", "price", "stock"]
    ):
        return jsonify({
            "error": "name, price and stock are required"
        }), 400

    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO products (name, price, stock)
        VALUES (?, ?, ?)
        """,
        (
            data["name"],
            data["price"],
            data["stock"]
        )
    )

    connection.commit()

    product_id = cursor.lastrowid

    product = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    connection.close()

    return jsonify(dict(product)), 201


@app.get("/products/<int:product_id>")
def get_product(product_id):
    connection = get_connection()

    product = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    connection.close()

    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify(dict(product)), 200


@app.put("/products/<int:product_id>")
def update_product(product_id):
    data = request.get_json()

    connection = get_connection()

    existing = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    if existing is None:
        connection.close()

        return jsonify({
            "error": "Product not found"
        }), 404

    connection.execute(
        """
        UPDATE products
        SET name = ?, price = ?, stock = ?
        WHERE id = ?
        """,
        (
            data["name"],
            data["price"],
            data["stock"],
            product_id
        )
    )

    connection.commit()

    product = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    connection.close()

    return jsonify(dict(product)), 200


@app.delete("/products/<int:product_id>")
def delete_product(product_id):
    connection = get_connection()

    existing = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    if existing is None:
        connection.close()

        return jsonify({
            "error": "Product not found"
        }), 404

    connection.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id,)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Product deleted"
    }), 200


@app.post("/orders")
def create_order():
    data = request.get_json()

    if not data or not all(
        key in data for key in ["product_id", "quantity"]
    ):
        return jsonify({
            "error": "product_id and quantity are required"
        }), 400

    connection = get_connection()

    product = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (data["product_id"],)
    ).fetchone()

    if product is None:
        connection.close()

        return jsonify({
            "error": "Product not found"
        }), 404

    total = product["price"] * data["quantity"]

    cursor = connection.execute(
        """
        INSERT INTO orders (product_id, quantity, total)
        VALUES (?, ?, ?)
        """,
        (
            data["product_id"],
            data["quantity"],
            total
        )
    )

    connection.commit()

    order = connection.execute(
        "SELECT * FROM orders WHERE id = ?",
        (cursor.lastrowid,)
    ).fetchone()

    connection.close()

    return jsonify(dict(order)), 201


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )