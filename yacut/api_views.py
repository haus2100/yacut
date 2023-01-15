from http import HTTPStatus
from re import fullmatch

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


INVALID_SHORT_LINK = 'Указано недопустимое имя для короткой ссылки'
MISSING_REQUEST_BODY = 'Отсутствует тело запроса'
SHORT_ID_NOT_FOUND = 'Указанный id не найден'
URL_IS_REQUIRED_FIELD = '"url" является обязательным полем!'


@app.route('/api/id/', methods=['POST'])
def create_url():
    PATTERN = r'^[a-zA-Z0-9]{1,16}$'

    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(MISSING_REQUEST_BODY)
    if not data.get('url'):
        raise InvalidAPIUsage(URL_IS_REQUIRED_FIELD)
    short_id = data.get('custom_id')
    if not short_id:
        data['custom_id'] = get_unique_short_id()
    elif URLMap.query.filter_by(short=short_id).first():
        raise InvalidAPIUsage(f'Имя "{short_id}" уже занято.')
    elif not fullmatch(PATTERN, short_id):
        raise InvalidAPIUsage(INVALID_SHORT_LINK)
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED.value


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage(
            SHORT_ID_NOT_FOUND, HTTPStatus.NOT_FOUND.value
        )
    return jsonify(url=url_map.original), HTTPStatus.OK.value
