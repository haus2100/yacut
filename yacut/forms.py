from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


CREATE = 'Создать'
CUSTOM_SHORT_LINK = 'Ваш вариант короткой ссылки'
LONG_LINK = 'Длинная ссылка'
REQUIRED_FIELD = 'Обязательное поле'


class URLForm(FlaskForm):
    original_link = URLField(
        LONG_LINK,
        validators=[DataRequired(message=REQUIRED_FIELD), ]
    )
    custom_id = StringField(
        CUSTOM_SHORT_LINK,
        validators=[Length(max=16), Optional()]
    )
    submit = SubmitField(CREATE)
