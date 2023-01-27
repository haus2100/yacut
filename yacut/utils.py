from functools import wraps
from typing import Iterable

from flask import request
from .exceptions import APIRequestError

from . import db
from . import constants as const


def save(obj):
    db.session.add(obj)
    db.session.commit()


def required_fields(
    fields: Iterable,
    message=(const.REQUIRED_FIELD),
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            if not data:
                raise APIRequestError(const.MISSING_REQUEST_BODY)
            for field in fields:
                if field not in data:
                    raise APIRequestError(message.format(field=field))
            return func(*args, **kwargs)
        return wrapper
    return decorator
