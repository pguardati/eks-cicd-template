import datetime
import functools
import logging

import jwt
from flask import request
from werkzeug.exceptions import abort


def _logger(log_level):
    """Setup logger format, level, and handler.

    Returns:
        logger
    """
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log = logging.getLogger(__name__)
    log.setLevel(log_level)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    log.addHandler(stream_handler)
    return log


def _get_jwt(user_data, jwt_secret):
    """Generate jwt token
    Args:
        user_data(dict): login data from user, format: {'email': email, 'password': password}

    Returns:
        str
    """
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(weeks=2)
    payload = {'exp': exp_time,
               'nbf': datetime.datetime.utcnow(),
               'email': user_data['email']}
    return jwt.encode(payload, jwt_secret, algorithm='HS256')


def require_jwt(function, jwt_secret):
    """Decorator to check valid jwt is present"""

    @functools.wraps(function)
    def decorated_function(*args, **kws):
        if not 'Authorization' in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = str.replace(str(data), 'Bearer ', '')
        try:
            jwt.decode(token, jwt_secret, algorithms=['HS256'])
        except:
            abort(401)

        return function(*args, **kws)

    return decorated_function
