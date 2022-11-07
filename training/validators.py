import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone


def validate_date_precedence(start_date, end_date, field_name=None):
    if start_date and end_date and start_date > end_date:
        msg = "End date cannot precede start date"
        if field_name:
            msg = {field_name: msg}
        raise ValidationError(msg, code="date_precedence")


def validate_start_date(start_date):
    if start_date < timezone.now().date():
        raise ValidationError("Start date has passed", code="start_date_in_the_past")


validate_identifier = RegexValidator(
    regex=re.compile(r"^[-a-z0-9]+$"),
    message="Training identifier contains illegal characters",
    code="invalid_identifier",
)
