import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    now = timezone.now().year
    if value > now:
        raise ValidationError(
            f'{value} не может быть больше {now}'
        )


def validate_slug(slug):
    if re.search(r'^[\w.@+-]+\Z', slug) is None:
        raise ValidationError(
            f'Не допустимые символы <{slug}> .'
        )
