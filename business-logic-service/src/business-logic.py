from flask import Flask, request, Response
from http import HTTPStatus
import requests
from utils import verify_request_body, verify_authorization, auth_url, core_url
import json

app = Flask(__name__)


@app.route("/business-logic/api/products", methods=["POST"])
def post_product():
    auth_validation = verify_authorization(
        request.headers.get("Authorization"))

    if auth_validation["status"] != HTTPStatus.OK:
        return Response(status=auth_validation["status"])

    current_user = auth_validation["user"]

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

    core_params = {
        "username": current_user["username"]
    }

    tag_ids = body.pop("tag_ids")
    body["vendor_id"] = (requests.get(
        f"{core_url}/core/vendors", params=core_params)).json()["vendor_id"]

    added_product_response = requests.post(
        f"{core_url}/core/products", json=body)

    if added_product_response.status_code == HTTPStatus.CREATED:
        body_tags = {
            "product_id": added_product_response.json()["product_id"],
            "tag_ids": tag_ids
        }

        requests.post(f"{core_url}/core/product_tags", json=body_tags)

    return Response(status=added_product_response.status_code)


@app.route("/business-logic/api/products", methods=["GET"])
def get_vendor_products():
    auth_validation = verify_authorization(
        request.headers.get("Authorization"))

    if auth_validation["status"] != HTTPStatus.OK:
        return Response(status=auth_validation["status"])

    current_user = auth_validation["user"]

    if "ROLE_VENDOR" not in current_user["roles"]:
        return Response(status=HTTPStatus.FORBIDDEN)

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

    return json.dumps(current_vendor_products.json()), HTTPStatus.OK


@app.route("/business-logic/api/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    auth_validation = verify_authorization(
        request.headers.get("Authorization"))

    if auth_validation["status"] != HTTPStatus.OK:
        return Response(status=auth_validation["status"])

    current_user = auth_validation["user"]

    if "ROLE_VENDOR" not in current_user["roles"]:
        return Response(status=HTTPStatus.FORBIDDEN)

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

    if not any(product["product_id"] == id for product in current_vendor_products.json()):
        return Response(status=HTTPStatus.NOT_FOUND)

    deleted_product_response = requests.delete(
        f"{core_url}/core/products/{id}")

    return Response(status=deleted_product_response.status_code)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
