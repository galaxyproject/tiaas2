from datetime import date
import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_date_precedence(start_date, end_date, field_name=None):
    if start_date and end_date and start_date > end_date:
        msg = 'End date cannot precede start date'
        if field_name:
            msg = {field_name: msg}
        raise ValidationError(msg, code='date_precedence')


def validate_start_date(start_date):
    if start_date < date.today():
        raise ValidationError('Start date has passed', code='start_date_in_the_past')


validate_identifier = RegexValidator(
    regex=re.compile(r'^[-a-z0-9_]+\Z'),
    message='Training identifier contains illegal characters',
    code='invalid_identifier'
)
