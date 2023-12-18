from Clients import FlaskClient
from flask import request, jsonify
from marshmallow import ValidationError

from schema.street_schema import StreetSchema
from trash_can_client import TrashCanClient

flask_client = FlaskClient()
app = flask_client.get_client()
client = TrashCanClient()


@app.route('/', methods=['GET'])
def index():
    schema = StreetSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 422
    if "add_on" not in data:
        data["add_on"] = ""
    return jsonify(
        client.get_data(data["zip_code"], data["house_number"], data["add_on"])
    )


@app.route('/', methods=['DELETE'])
def cleanup():
    try:
        client.cleanup()
    except:
        return jsonify(
            {
                "message": "Collections not found"
            }
        ), 404

    return jsonify(
        {
            "message": "Collections cleaned up"
        }
    )


@app.route('/<key>', methods=['DELETE'])
def cleanup_collection(key):
    try:
        client.cleanup_collection(key)
    except:
        return jsonify(
            {
                "message": "Collection not found"
            }
        ), 404
    return jsonify(
        {
            "message": f"Collection {key} cleaned up"
        }
    )


if __name__ == '__main__':
    app.run(
        port=flask_client.get_port(),
        debug=flask_client.get_debug(),
        host=flask_client.get_host()
    )
