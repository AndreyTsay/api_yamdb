import re

from django.core.exceptions import ValidationError


def validate_slug(username):
    if username == 'me':
        raise ValidationError('Недопустимое имя пользователя!')

    if re.search(r'^[\w.@+-]+\Z', username) is None:
        raise ValidationError(
            f'Не допустимые символы <{username}> в нике.'
        )
