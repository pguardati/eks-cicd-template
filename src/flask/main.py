import jwt

from flask import Flask, jsonify, request, abort
from src.constants import LOG_LEVEL, JWT_SECRET
from src.utils import _logger, _get_jwt

LOG = _logger(LOG_LEVEL)
LOG.debug("Starting with log level: %s" % LOG_LEVEL)
APP = Flask(__name__)


@APP.route('/', methods=['POST', 'GET'])
def health():
    return jsonify("Healthy")


@APP.route('/auth', methods=['POST'])
def auth():
    """Create JWT token based on email.

        URL:
            /auth
        Method:
            POST
        URL Params:
            None
        Data Params::
            None

        Success Response::

            Code: 200
            Content:
            {
              "token": "eyJ0ODbe...NgfW3_vibQWTffblx8"
            }

        Error Response::

            None

        Sample Call::

             curl -X POST \
             -d '{"email": "my_mail","password": "my_pass"}' \
             -H 'Content-Type: application/json' \
             -v http://localhost:80/auth
    """
    request_data = request.get_json()
    email = request_data.get('email')
    password = request_data.get('password')
    if not email:
        LOG.error("No email provided")
        return jsonify({"message": "Missing parameter: email"}, 400)
    if not password:
        LOG.error("No password provided")
        return jsonify({"message": "Missing parameter: password"}, 400)
    body = {'email': email, 'password': password}
    if not JWT_SECRET:
        LOG.error("Missing Secret")
        return jsonify({"message": "Missing environment variable: JWT_SECRET"}, 400)
    user_data = body
    return jsonify(token=_get_jwt(user_data, JWT_SECRET).decode('utf-8'))


@APP.route('/contents', methods=['GET'])
def decode_jwt():
    """Check user token and return non-secret data

        URL:
            /contents
        Method:
            GET
        URL Params:
            None
        Data Params::
            None

        Success Response::

            Code: 200
            Content:
            {
                "email": "wolf@thedoor.com",
                "exp": 1610557267,
                "nbf": 1609347667
            }

        Error Response::

            Code: 401

        Sample Call::

             curl -X GET \
             -H "Authorization: Bearer ${TOKEN}" \
             -v http://localhost:80/contents

    """
    if not 'Authorization' in request.headers:
        abort(401)
    data = request.headers['Authorization']
    token = str.replace(str(data), 'Bearer ', '')
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except:
        abort(401)
    response = {'email': data['email'],
                'exp': data['exp'],
                'nbf': data['nbf']}
    return jsonify(**response)


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=80, debug=True)
