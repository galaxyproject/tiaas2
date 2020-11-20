from datetime import date
from django.core.exceptions import ValidationError


def validate_date_precedence(start_date, end_date, field_name=None):
    if start_date and end_date and start_date > end_date:
        msg = 'End date cannot precede start date'
        if field_name:
            msg = {field_name: msg}
        raise ValidationError(msg, code='DATE_PRECEDENCE')


def validate_start_date(start_date):
    if start_date < date.today():
        raise ValidationError('Start date has passed', code='START_DATE_IN_THE_PAST')
