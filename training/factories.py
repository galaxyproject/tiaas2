"""Create fake records for development."""

import datetime
import random

import factory
from factory import lazy_attribute
from factory.django import DjangoModelFactory

from .models import Training

START_IN_DAYS_MIN = 0
START_IN_DAYS_MAX = 180


class TrainingFactory(DjangoModelFactory):
    """Create fake trainings."""

    class Meta:
        model = Training
        django_get_or_create = ["training_identifier"]

    class Params:
        start_min_days = START_IN_DAYS_MIN
        start_max_days = START_IN_DAYS_MAX

    @lazy_attribute
    def start(self):
        return datetime.date.today() + datetime.timedelta(
            days=random.randint(self.start_min_days, self.start_max_days,)
        )

    received = factory.Faker("date")
    name = factory.Faker("name")
    email = factory.Faker("email")
    title = factory.Faker("sentence", nb_words=5, variable_nb_words=True,)
    description = factory.Faker("sentence", nb_words=50, variable_nb_words=True,)
    end = lazy_attribute(
        lambda o: o.start + datetime.timedelta(days=random.randint(0, 7))
    )
    website = factory.Faker("ascii_email")
    location = factory.Faker("country_code")
    use_gtn = factory.Faker("random_element", elements=["Y", "N"],)
    gtn_links = factory.Faker("sentence", nb_words=50, variable_nb_words=True,)
    non_gtn_links = factory.Faker("sentence", nb_words=50, variable_nb_words=True,)
    attendance = factory.Faker("random_int", min=1, max=100,)
    training_identifier = factory.Faker("word")
    advertise = factory.Faker("random_element", elements=["Y", "N"],)
    # These can probably both use the default:
    # retain_contact = factory.Faker()
    # blogpost = factory.Faker()
    other_requests = factory.Faker("sentence", nb_words=50, variable_nb_words=True,)
    processed = factory.Faker("random_element", elements=["UN", "AP", "RE"],)
