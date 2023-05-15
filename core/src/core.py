from flask import Flask, request, Response
from http import HTTPStatus
from utils import verify_request_body
import json
import psycopg2
import os


app = Flask(__name__)

connection = psycopg2.connect(
    host=os.getenv("PGHOST"),
    port=int(os.getenv("PGPORT")),
    database=os.getenv("PGDATABASE"),
    user=os.getenv("PGUSER"),
    password=os.getenv("PGPASS")
)

################################ PRODUCT TABLE #################################


@app.route("/core/products/<int:id>", methods=["GET"])
def get_product(id):
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM product WHERE product_id = {id}")
    product_column_names = [desc[0] for desc in cursor.description]
    product_row = cursor.fetchone()

    # verifies the given product exists and returns otherwise
    if product_row == None:
        return Response(status=HTTPStatus.NOT_FOUND)

    # gets product tags
    cursor.execute(
        f"SELECT tag_id FROM product_tag WHERE product_id = {product_row[0]}")
    tag_ids = [tag_row[0] for tag_row in cursor]

    product = dict(zip(product_column_names, product_row))
    product["tag_ids"] = tag_ids

    return json.dumps(product), HTTPStatus.OK


@app.route("/core/products", methods=["GET"])
def get_products():
    # possible products filters/arguments
    product_category_id = request.args.get("product_category_id")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    availability = request.args.get("availability")
    vendor_id = request.args.get("vendor_id")
    tag_ids = request.args.get("tag_ids")
    product_search_name = request.args.get("product_search_name")

    query = "SELECT DISTINCT ON (product_id) * FROM product"
    filters = []

    if not product_category_id is None:
        filters.append(f"product_category_id = {product_category_id}")

    if not min_price is None:
        filters.append(f"price >= {min_price}")

    if not max_price is None:
        filters.append(f"price <= {max_price}")

    if not availability is None:
        filters.append(f"availability = \'{availability}\'")

    if not vendor_id is None:
        filters.append(f"vendor_id = {vendor_id}")

    if not product_search_name is None:
        filters.append(
            f"LOWER(product_name) LIKE \'%{product_search_name.lower()}%\'")

    if not tag_ids is None:
        query += " NATURAL JOIN product_tag"
        filters.append(f"tag_id IN ({tag_ids})")

    if len(filters) > 0:
        query += f" WHERE {filters[0]}"

        for filter in filters[1:]:
            query += f" AND {filter}"

    cursor = connection.cursor()

    try:
        cursor.execute(query)
    except:
        return Response(status=HTTPStatus.BAD_REQUEST)

    product_column_names = [desc[0] for desc in cursor.description]
    product_rows = cursor.fetchall()

    # creates filtered products list
    products = []
    for product_row in product_rows:
        cursor.execute(
            f"SELECT tag_id FROM product_tag WHERE product_id = {product_row[0]}")
        tag_ids = [tag_row[0] for tag_row in cursor]

        product = dict(zip(product_column_names, product_row))
        product["tag_ids"] = tag_ids

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
            f"INSERT INTO product (vendor_id, product_category_id, product_name, description, price, availability) VALUES ({vendor_id}, {product_category_id}, '{product_name}', '{description}', {price}, '{availability}') RETURNING product_id"
        )
    # treats unique key violation
    except psycopg2.errors.UniqueViolation:
        connection.rollback()
        return Response(status=HTTPStatus.CONFLICT)
    # treats any other error
    except:
        connection.rollback()
        return Response(status=HTTPStatus.BAD_REQUEST)

    new_product = {
        "product_id": cursor.fetchone()[0]
    }

    connection.commit()

    return json.dumps(new_product), HTTPStatus.CREATED


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


############################## PRODUCT_TAG TABLE ###############################


@app.route("/core/product_tags", methods=["POST"])
def add_product_tag():
    body = request.get_json()

    if not verify_request_body(
        body,
        [
            "product_id",
            "tag_id"
        ],
    ):
        return Response(status=HTTPStatus.BAD_REQUEST)

    cursor = connection.cursor()

    product_id = body["product_id"]
    tag_id = body["tag_id"]

    try:
        cursor.execute(
            f"INSERT INTO product_tag VALUES ({product_id}, {tag_id})"
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


################################ CUSTOMER TABLE ################################


@app.route("/core/customers", methods=["POST"])
def add_customer():
    body = request.get_json()

    if not verify_request_body(
        body,
        [
            "email",
            "firstName",
            "lastName"
        ],
    ):
        return Response(status=HTTPStatus.BAD_REQUEST)

    email = body["email"]
    first_name = body["firstName"]
    last_name = body["lastName"]

    cursor = connection.cursor()

    try:
        cursor.execute(
            f"INSERT INTO customer (email, first_name, last_name) VALUES ('{email}', '{first_name}', '{last_name}') RETURNING customer_id"
        )
    # treats unique key violation
    except psycopg2.errors.UniqueViolation:
        connection.rollback()
        return Response(status=HTTPStatus.CONFLICT)
    # treats any other error
    except:
        connection.rollback()
        return Response(status=HTTPStatus.BAD_REQUEST)

    customer_id = cursor.fetchone()[0]

    # creates customer cart
    cursor.execute(
        f"INSERT INTO cart (customer_id) VALUES ({customer_id}) RETURNING cart_id"
    )

    cart_id = cursor.fetchone()[0]

    connection.commit()

    new_customer = {
        "customer_id": customer_id,
        "cart_id": cart_id
    }

    return json.dumps(new_customer), HTTPStatus.CREATED


@app.route("/core/customers", methods=["GET"])
def get_customer_by_email():
    customer_email = request.args.get("username")

    if customer_email is None:
        return Response(status=HTTPStatus.BAD_REQUEST)

    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM customer WHERE email = '{customer_email}'")
    customer_row = cursor.fetchone()

    # verifies the given customer exists
    if customer_row == None:
        return Response(status=HTTPStatus.NOT_FOUND)

    customer = {
        "customer_id": customer_row[0]
    }

    return json.dumps(customer), HTTPStatus.OK


################################# VENDOR TABLE #################################


@app.route("/core/vendors", methods=["POST"])
def add_vendor():
    body = request.get_json()

    if not verify_request_body(
        body,
        [
            "email",
            "companyName",
            "companyAddress",
            "bankAccount"
        ],
    ):
        return Response(status=HTTPStatus.BAD_REQUEST)

    email = body["email"]
    company_name = body["companyName"]
    company_address = body["companyAddress"]
    bank_account = body["bankAccount"]

    cursor = connection.cursor()

    try:
        cursor.execute(
            f"INSERT INTO vendor (email, company_name, company_address, bank_account) VALUES ('{email}', '{company_name}', '{company_address}', '{bank_account}')"
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


@app.route("/core/vendors", methods=["GET"])
def get_vendor_by_email():
    vendor_email = request.args.get("username")

    if vendor_email is None:
        return Response(status=HTTPStatus.BAD_REQUEST)

    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM vendor WHERE email = '{vendor_email}'")
    vendor_row = cursor.fetchone()

    # verifies the given vendor exists
    if vendor_row == None:
        return Response(status=HTTPStatus.NOT_FOUND)

    vendor = {
        "vendor_id": vendor_row[0]
    }

    return json.dumps(vendor), HTTPStatus.OK


############################## CART_PRODUCT TABLE ##############################


@app.route("/core/cart-products", methods=["POST"])
def add_cart_product():
    body = request.get_json()

    if not verify_request_body(
        body,
        [
            "cart_id",
            "product_id",
            "quantity"
        ],
    ):
        return Response(status=HTTPStatus.BAD_REQUEST)

    cart_id = body["cart_id"]
    product_id = body["product_id"]
    quantity = body["quantity"]

    cursor = connection.cursor()

    cursor.execute(
        f"SELECT quantity FROM cart_product WHERE cart_id = {cart_id} AND product_id = {product_id}")
    cart_product_row = cursor.fetchone()

    # verifies the product does not exist in the cart already
    if cart_product_row == None:
        try:
            cursor.execute(
                f"INSERT INTO cart_product (cart_id, product_id, quantity) VALUES ({cart_id}, {product_id}, {quantity})"
            )
        # treats any error
        except:
            connection.rollback()
            return Response(status=HTTPStatus.BAD_REQUEST)
    else:
        new_quantity = cart_product_row[0] + quantity

        cursor.execute(
            f"UPDATE cart_product SET quantity = {new_quantity} WHERE cart_id = {cart_id} AND product_id = {product_id}"
        )

    # updates cart total price
    cursor.execute(
        f"SELECT price FROM product WHERE product_id = {product_id}")
    product_price = cursor.fetchone()[0]

    cursor.execute(f"SELECT total_price FROM cart WHERE cart_id = {cart_id}")
    current_total_price = cursor.fetchone()[0]

    new_total_price = current_total_price + product_price * quantity

    cursor.execute(
        f"UPDATE cart SET total_price = {new_total_price} WHERE cart_id = {cart_id}"
    )

    connection.commit()

    return Response(status=HTTPStatus.CREATED)


@app.route("/core/cart-products", methods=["GET"])
def get_cart_products():
    cart_id = request.args.get("cart_id")

    if cart_id is None:
        return Response(status=HTTPStatus.BAD_REQUEST)

    cursor = connection.cursor()

    cursor.execute(
        f"SELECT * FROM cart WHERE cart_id = {cart_id}")
    cart_row = cursor.fetchone()

    # cart does not exist
    if cart_row is None:
        return Response(status=HTTPStatus.BAD_REQUEST)

    cursor.execute(
        f"SELECT * FROM cart_product WHERE cart_id = {cart_id}")
    cart_product_rows = cursor.fetchall()

    cart_products = []
    for cart_product_row in cart_product_rows:
        cart_product = {
            "product_id": cart_product_row[1],
            "quantity": cart_product_row[2]
        }
        cart_products.append(cart_product)

    return json.dumps(cart_products), HTTPStatus.OK


@app.route("/core/cart-products/<int:cart_id>/<int:product_id>", methods=["DELETE"])
def delete_cart_product(cart_id, product_id):
    cursor = connection.cursor()

    cursor.execute(
        f"SELECT * FROM cart WHERE cart_id = {cart_id}")
    cart_row = cursor.fetchone()

    # cart does not exist
    if cart_row is None:
        return Response(status=HTTPStatus.NOT_FOUND)

    cursor.execute(
        f"DELETE FROM cart_product WHERE product_id = {product_id} AND cart_id = {cart_id} RETURNING quantity")

    deleted_rows = cursor.rowcount
    # verifies the given product exists
    if deleted_rows == 0:
        return Response(status=HTTPStatus.NOT_FOUND)

    quantity = cursor.fetchone()[0]

    # updates cart total price
    cursor.execute(
        f"SELECT price FROM product WHERE product_id = {product_id}")
    product_price = cursor.fetchone()[0]

    cursor.execute(f"SELECT total_price FROM cart WHERE cart_id = {cart_id}")
    current_total_price = cursor.fetchone()[0]

    new_total_price = current_total_price - product_price * quantity

    cursor.execute(
        f"UPDATE cart SET total_price = {new_total_price} WHERE cart_id = {cart_id}"
    )

    connection.commit()

    return Response(status=HTTPStatus.OK)


################################## CART TABLE ##################################


@app.route("/core/carts", methods=["GET"])
def get_customer_current_cart():
    customer_id = request.args.get("customer_id")

    if customer_id is None:
        return Response(status=HTTPStatus.BAD_REQUEST)

    cursor = connection.cursor()

    cursor.execute(
        f"SELECT * FROM cart WHERE customer_id = {customer_id} AND status = \'current\'")
    cart_column_names = [desc[0] for desc in cursor.description]
    cart_row = cursor.fetchone()

    if cart_row is None:
        return Response(status=HTTPStatus.NOT_FOUND)

    cart = dict(zip(cart_column_names, cart_row))

    return json.dumps(cart), HTTPStatus.OK


################################# ORDER TABLE ##################################


@app.route("/core/orders", methods=["POST"])
def add_order():
    body = request.get_json()

    if not verify_request_body(
        body,
        [
            "cart_id",
            "order_date",
            "total_price",
            "shipping_address",
            "customer_bank_account"
        ],
    ):
        return Response(status=HTTPStatus.BAD_REQUEST)

    cart_id = body["cart_id"]
    order_date = body["order_date"]
    total_price = body["total_price"]
    shipping_address = body["shipping_address"]
    customer_bank_account = body["customer_bank_account"]

    cursor = connection.cursor()

    try:
        cursor.execute(
            f"INSERT INTO \"order\" (cart_id, order_date, total_price, shipping_address, customer_bank_account) VALUES ({cart_id}, '{order_date}', {total_price}, '{shipping_address}', '{customer_bank_account}') RETURNING order_id"
        )
    # treats unique key violation
    except psycopg2.errors.UniqueViolation:
        connection.rollback()
        return Response(status=HTTPStatus.CONFLICT)
    # treats any other error
    except:
        connection.rollback()
        return Response(status=HTTPStatus.BAD_REQUEST)

    new_order = {
        "order_id": cursor.fetchone()[0]
    }

    # mark cart as ordered
    cursor.execute(
        f"UPDATE cart SET status = 'old' WHERE cart_id = {cart_id} RETURNING customer_id"
    )

    customer_id = cursor.fetchone()[0]

    # creates customer new cart
    cursor.execute(
        f"INSERT INTO cart (customer_id) VALUES ({customer_id}) RETURNING cart_id"
    )

    new_order["cart_id"] = cursor.fetchone()[0]

    connection.commit()

    return json.dumps(new_order), HTTPStatus.CREATED


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7000)
