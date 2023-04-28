from flask import Flask, request, Response
from http import HTTPStatus
from utils import verify_request_body
import json
import psycopg2


app = Flask(__name__)

# TODO: replace fields with env variables (check values match docker compose)
connection = psycopg2.connect(
    host="postgres_container",
    port=5432,
    database="FlowerShopDB",
    user="admin",
    password="admin"
)


@app.route("/core/products/<int:id>", methods=["GET"])
def get_product(id):
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM product WHERE product_id = {id}")
    product_row = cursor.fetchone()

    # verifies the given product exists
    if product_row == None:
        return Response(status=HTTPStatus.NOT_FOUND)

    cursor.execute(
        f"SELECT company_name FROM vendor WHERE vendor_id = {product_row[1]}"
    )
    vendor_row = cursor.fetchone()

    product = {
        "flower": product_row[3],
        "description": product_row[4],
        "price": product_row[5],
        "availability": product_row[6],
        "vendor": vendor_row[0],
    }

    return json.dumps(product), HTTPStatus.OK


@app.route("/core/products", methods=["GET"])
def get_products():
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM product")
    product_rows = cursor.fetchall()

    products = []
    for product_row in product_rows:
        cursor.execute(
            f"SELECT company_name FROM vendor WHERE vendor_id = {product_row[1]}"
        )
        vendor_row = cursor.fetchone()

        product = {
            "id": product_row[0],
            "flower": product_row[3],
            "description": product_row[4],
            "price": product_row[5],
            "availability": product_row[6],
            "vendor": vendor_row[0],
        }
        products.append(product)

    return json.dumps(products), HTTPStatus.OK


@app.route("/core/products", methods=["POST"])
def add_product():
    body = request.get_json()

    if not verify_request_body(
        body,
        [
            "vendor_id",
            "product_category_id",
            "product_name",
            "description",
            "price",
            "availability",
        ],
    ):
        return Response(status=HTTPStatus.BAD_REQUEST)

    vendor_id = body["vendor_id"]
    product_category_id = body["product_category_id"]
    product_name = body["product_name"]
    description = body["description"]
    price = body["price"]
    availability = body["availability"]

    cursor = connection.cursor()

    try:
        cursor.execute(
            f"INSERT INTO product (vendor_id, product_category_id, product_name, description, price, availability) VALUES ({vendor_id}, {product_category_id}, '{product_name}', '{description}', {price}, '{availability}')"
        )
    # treats unique key violation
    except psycopg2.errors.UniqueViolation:
        connection.rollback()
        return Response(status=HTTPStatus.CONFLICT)
    # treats any other error
    except:
        connection.rollback()
        return Response(status=HTTPStatus.BAD_REQUEST)

    connection.commit()

    return Response(status=HTTPStatus.CREATED)


@app.route("/core/products/<int:id>", methods=["PUT"])
def update_product(id):
    body = request.get_json()

    if not verify_request_body(
        body,
        [
            "vendor_id",
            "product_category_id",
            "product_name",
            "description",
            "price",
            "availability",
        ],
    ):
        return Response(status=HTTPStatus.BAD_REQUEST)

    vendor_id = body["vendor_id"]
    product_category_id = body["product_category_id"]
    product_name = body["product_name"]
    description = body["description"]
    price = body["price"]
    availability = body["availability"]

    cursor = connection.cursor()

    try:
        cursor.execute(
            f"UPDATE product SET vendor_id = {vendor_id}, product_category_id = {product_category_id}, product_name = '{product_name}', description = '{description}', price = {price}, availability = '{availability}' WHERE product_id = {id}"
        )
    # treats unique key violation
    except psycopg2.errors.UniqueViolation:
        connection.rollback()
        return Response(status=HTTPStatus.CONFLICT)
    # treats any other error
    except:
        connection.rollback()
        return Response(status=HTTPStatus.BAD_REQUEST)

    updated_rows = cursor.rowcount
    # verifies the given product exists
    if updated_rows == 0:
        return Response(status=HTTPStatus.NOT_FOUND)

    connection.commit()

    return Response(status=HTTPStatus.OK)


@app.route("/core/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    cursor = connection.cursor()

    cursor.execute(f"DELETE FROM product WHERE product_id = {id}")

    deleted_rows = cursor.rowcount
    # verifies the given product exists
    if deleted_rows == 0:
        return Response(status=HTTPStatus.NOT_FOUND)

    connection.commit()

    return Response(status=HTTPStatus.OK)

# TODO: check port is correct
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7000)