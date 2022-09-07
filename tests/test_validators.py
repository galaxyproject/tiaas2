import unittest
from datetime import date, timedelta

from django.core.exceptions import ValidationError

from training.validators import (
    validate_date_precedence,
    validate_identifier,
    validate_start_date,
)


class ValidatorsTestCase(unittest.TestCase):

    def test_validate_date_precedence_raise_error(self):
        # Expect error: end date < start date
        start_date = date(2100, 1, 2)
        end_date = date(2100, 1, 1)
        with self.assertRaises(ValidationError):
            validate_date_precedence(start_date, end_date)

    def test_validate_date_precedence(self):
        start_date = date(1892, 1, 3)
        end_date = date(1892, 1, 3)
        validate_date_precedence(start_date, end_date)

    def test_validate_start_date(self):
        # Expect error: start date < today
        start_date = date.today() - timedelta(days=1)
        with self.assertRaises(ValidationError):
            validate_start_date(start_date)

    def test_validate_identifier(self):
        validate_identifier('foo123')

        with self.assertRaises(ValidationError):
            validate_identifier('foo 123')  # space

        with self.assertRaises(ValidationError):
            validate_identifier('foo@123')  # special character

        with self.assertRaises(ValidationError):
            validate_identifier('Foo123')  # uppercase
