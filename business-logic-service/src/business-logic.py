from flask import Flask, request, Response
from http import HTTPStatus
import requests
from utils import verify_request_body, verify_authorization, core_url
import json
from datetime import date

app = Flask(__name__)


@app.route("/api/products", methods=["POST"])
def post_product():
    """
        Posts a new product. Action permitted only to vendor users.

        The body of the request contains all product data.
    """

    # auth verification
    auth_validation = verify_authorization(
        request.headers.get("Authorization"))

    if auth_validation["status"] != HTTPStatus.OK:
        return Response(status=auth_validation["status"])

    current_user = auth_validation["user"]

    # verifies current user role to include vendor priviledges
    if "ROLE_VENDOR" not in current_user["roles"]:
        return Response(status=HTTPStatus.FORBIDDEN)

    body = request.get_json()

    if not verify_request_body(
        body,
        [
            "product_category_id",
            "product_name",
            "description",
            "price",
            "availability",
            "tag_ids"
        ],
    ):
        return Response(status=HTTPStatus.BAD_REQUEST)

    # gets current user id
    core_params = {
        "username": current_user["username"]
    }

    tag_ids = body.pop("tag_ids")
    body["vendor_id"] = (requests.get(
        f"{core_url}/core/vendors", params=core_params)).json()["vendor_id"]

    # post a product
    added_product_response = requests.post(
        f"{core_url}/core/products", json=body)

    if added_product_response.status_code == HTTPStatus.CREATED:
        # if successful, adds product tags
        for tag_id in tag_ids:
            body = {
                "product_id": added_product_response.json()["product_id"],
                "tag_id": tag_id
            }

            requests.post(f"{core_url}/core/product_tags", json=body)

        return json.dumps(added_product_response.json()), HTTPStatus.CREATED

    return Response(status=added_product_response.status_code)


@app.route("/api/products/me", methods=["GET"])
def get_vendor_products():
    """
        Returns all products posted by the current user. Action permitted only to vendor users.
    """

    # auth verification
    auth_validation = verify_authorization(
        request.headers.get("Authorization"))

    if auth_validation["status"] != HTTPStatus.OK:
        return Response(status=auth_validation["status"])

    current_user = auth_validation["user"]

    # verifies current user role to include vendor priviledges
    if "ROLE_VENDOR" not in current_user["roles"]:
        return Response(status=HTTPStatus.FORBIDDEN)

    # gets current user id
    core_params = {
        "username": current_user["username"]
    }

    vendor_id = requests.get(
        f"{core_url}/core/vendors", params=core_params).json()["vendor_id"]

    core_params = {
        "vendor_id": vendor_id
    }

    # gets all products posted by current user
    current_vendor_products = requests.get(
        f"{core_url}/core/products", params=core_params)

    return json.dumps(current_vendor_products.json()), HTTPStatus.OK


@app.route("/api/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    """
        Deletes a posted product. Action permitted only to vendor users.

        The url contains the id of the product to be deleted.
    """

    # auth verification
    auth_validation = verify_authorization(
        request.headers.get("Authorization"))

    if auth_validation["status"] != HTTPStatus.OK:
        return Response(status=auth_validation["status"])

    current_user = auth_validation["user"]

    # verifies current user role to include vendor priviledges
    if "ROLE_VENDOR" not in current_user["roles"]:
        return Response(status=HTTPStatus.FORBIDDEN)

    # gets current user id
    core_params = {
        "username": current_user["username"]
    }

    vendor_id = requests.get(
        f"{core_url}/core/vendors", params=core_params).json()["vendor_id"]

    core_params = {
        "vendor_id": vendor_id
    }

    current_vendor_products = requests.get(
        f"{core_url}/core/products", params=core_params)

    # verifies the given product exists
    if not any(product["product_id"] == id for product in current_vendor_products.json()):
        return Response(status=HTTPStatus.NOT_FOUND)

    # deletes the product
    deleted_product_response = requests.delete(
        f"{core_url}/core/products/{id}")

    return Response(status=deleted_product_response.status_code)


@app.route("/api/products", methods=["GET"])
def get_products():
    """
        Returns all posted products. Action permitted to all users.

        The endpoint accepts parameters which can be used for product filtering and searching.

        ---
        filtering:
            product_category_id
            min_price
            max_price
            availability
            vendor_id
            tag_ids

        searching:
            product_search_name
    """

    # auth verification
    auth_validation = verify_authorization(
        request.headers.get("Authorization"))

    if auth_validation["status"] != HTTPStatus.OK:
        return Response(status=auth_validation["status"])

    # gets all products
    products = requests.get(f"{core_url}/core/products", params=request.args)

    return json.dumps(products.json()), HTTPStatus.OK


@app.route("/api/products/<int:id>", methods=["GET"])
def get_product(id):
    """
        Returns one posted product. Action permitted to all users.

        The url contains the id of the product to be returned.
    """

    # auth verification
    auth_validation = verify_authorization(
        request.headers.get("Authorization"))

    if auth_validation["status"] != HTTPStatus.OK:
        return Response(status=auth_validation["status"])

    # gets the product
    product = requests.get(f"{core_url}/core/products/{id}")

    # verifies the product exists
    if product.status_code != HTTPStatus.OK:
        return Response(status=product.status_code)

    return json.dumps(product.json()), HTTPStatus.OK


@app.route("/api/cart-products", methods=["POST"])
def add_cart_product():
    """
        Adds a product to customer cart. Action permitted only to customer users.

        The body of the request contains the product_id and the quantity to be added to cart.
    """

    # auth verification
    auth_validation = verify_authorization(
        request.headers.get("Authorization"))

    if auth_validation["status"] != HTTPStatus.OK:
        return Response(status=auth_validation["status"])

    # verifies current user role to include customer priviledges
    current_user = auth_validation["user"]

    if "ROLE_CUSTOMER" not in current_user["roles"]:
        return Response(status=HTTPStatus.FORBIDDEN)

    body = request.get_json()

    if not verify_request_body(
        body,
        [
            "product_id",
            "quantity"
        ],
    ):
        return Response(status=HTTPStatus.BAD_REQUEST)

    # verifies the product exists
    product_id = body["product_id"]
    product = requests.get(f"{core_url}/core/products/{product_id}")

    if product.status_code != HTTPStatus.OK:
        return Response(status=product.status_code)

    # verifies the product is in stock
    if product.json()["availability"] == "out of stock":
        return Response(status=HTTPStatus.BAD_REQUEST)

    # gets current user id
    core_params = {
        "username": current_user["username"]
    }

    customer_id = requests.get(
        f"{core_url}/core/customers", params=core_params).json()["customer_id"]

    core_params = {
        "customer_id": customer_id
    }

    # gets customer current cart
    cart_id = requests.get(
        f"{core_url}/core/carts", params=core_params).json()["cart_id"]

    body["cart_id"] = cart_id

    # adds product to cart
    added_cart_product_response = requests.post(
        f"{core_url}/core/cart-products", json=body)

    return Response(status=added_cart_product_response.status_code)


@app.route("/api/cart-products/<int:id>", methods=["DELETE"])
def delete_cart_product(id):
    """
        Deletes a product from user cart. Action permitted only to customer users.

        The url contains the id of the product to be deleted.
    """

    # auth verification
    auth_validation = verify_authorization(
        request.headers.get("Authorization"))

    if auth_validation["status"] != HTTPStatus.OK:
        return Response(status=auth_validation["status"])

    # verifies current user role to include customer priviledges
    current_user = auth_validation["user"]

    if "ROLE_CUSTOMER" not in current_user["roles"]:
        return Response(status=HTTPStatus.FORBIDDEN)

    # gets current user id
    core_params = {
        "username": current_user["username"]
    }

    customer_id = requests.get(
        f"{core_url}/core/customers", params=core_params).json()["customer_id"]

    # gets customer current cart
    core_params = {
        "customer_id": customer_id
    }

    cart_id = requests.get(
        f"{core_url}/core/carts", params=core_params).json()["cart_id"]

    # deletes product from cart
    deleted_cart_product_response = requests.delete(
        f"{core_url}/core/cart-products/{cart_id}/{id}")

    return Response(status=deleted_cart_product_response.status_code)


@app.route("/api/carts", methods=["GET"])
def get_cart():
    """
        Returns products from user cart. Action permitted only to customer users.
    """

    # auth verification
    auth_validation = verify_authorization(
        request.headers.get("Authorization"))

    if auth_validation["status"] != HTTPStatus.OK:
        return Response(status=auth_validation["status"])

    # verifies current user role to include customer priviledges
    current_user = auth_validation["user"]

    if "ROLE_CUSTOMER" not in current_user["roles"]:
        return Response(status=HTTPStatus.FORBIDDEN)

    # gets current user id
    core_params = {
        "username": current_user["username"]
    }

    customer_id = requests.get(
        f"{core_url}/core/customers", params=core_params).json()["customer_id"]

    # gets customer current cart
    core_params = {
        "customer_id": customer_id
    }

    cart = requests.get(
        f"{core_url}/core/carts", params=core_params).json()

    # gets current customer cart products
    core_params = {
        "cart_id": cart["cart_id"]
    }

    cart_products = requests.get(
        f"{core_url}/core/cart-products", params=core_params)

    if cart_products.status_code != HTTPStatus.OK:
        return Response(status=cart_products.status_code)

    cart_response = {
        "cart_id": cart["cart_id"],
        "total_price": cart["total_price"],
        "cart_products": cart_products.json()
    }

    return json.dumps(cart_response), HTTPStatus.OK


@app.route("/api/orders", methods=["POST"])
def add_order():
    """
        Orders the items found in the current user cart. Action permitted only to customer users.

        The body of the request contains the customer shipping and payment information.
    """

    # auth verification
    auth_validation = verify_authorization(
        request.headers.get("Authorization"))

    if auth_validation["status"] != HTTPStatus.OK:
        return Response(status=auth_validation["status"])

    # verifies current user role to include customer priviledges
    current_user = auth_validation["user"]

    if "ROLE_CUSTOMER" not in current_user["roles"]:
        return Response(status=HTTPStatus.FORBIDDEN)

    body = request.get_json()

    if not verify_request_body(
        body,
        [
            "shipping_address",
            "customer_bank_account"
        ],
    ):
        return Response(status=HTTPStatus.BAD_REQUEST)

    # gets current user id
    core_params = {
        "username": current_user["username"]
    }

    customer_id = requests.get(
        f"{core_url}/core/customers", params=core_params).json()["customer_id"]

    core_params = {
        "customer_id": customer_id
    }

    # gets customer current cart
    cart_response = requests.get(
        f"{core_url}/core/carts", params=core_params).json()
    
    # verify cart is empty
    if cart_response["total_price"] == 0:
        return Response(status=HTTPStatus.BAD_REQUEST)

    cart_id = cart_response["cart_id"]
    order_date = date.today().strftime("%Y-%m-%d")
    total_price = cart_response["total_price"] + 20  # shipping tax

    body["cart_id"] = cart_id
    body["order_date"] = order_date
    body["total_price"] = total_price

    # orders cart products
    added_order_response = requests.post(
        f"{core_url}/core/orders", json=body)

    if added_order_response.status_code != HTTPStatus.CREATED:
        return Response(status=added_order_response.status_code)

    return json.dumps(added_order_response.json()), HTTPStatus.CREATED


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
