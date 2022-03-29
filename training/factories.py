"""Create fake records for development."""

import random
import factory
import datetime
from factory import lazy_attribute
from factory.django import DjangoModelFactory

from .models import Training


class TrainingFactory(DjangoModelFactory):
    """Create fake trainings."""

    class Meta:
        model = Training

    @lazy_attribute
    def start(self):
        return (
            datetime.date.today()
            + datetime.timedelta(
                days=random.randint(-30, 120))
        )

    received = factory.Faker('date')
    name = factory.Faker('name')
    email = factory.Faker('email')
    title = factory.Faker(
        'sentence',
        nb_words=5,
        variable_nb_words=True,
    )
    description = factory.Faker(
        'sentence',
        nb_words=50,
        variable_nb_words=True,
    )
    end = lazy_attribute(
        lambda o: o.start + datetime.timedelta(
            days=random.randint(0, 7)
        )
    )
    website = factory.Faker('ascii_email')
    location = factory.Faker('country')
    use_gtn = factory.Faker(
        'random_element',
        elements=['Y', 'N'],
    )
    gtn_links = factory.Faker(
        'sentence',
        nb_words=50,
        variable_nb_words=True,
    )
    non_gtn_links = factory.Faker(
        'sentence',
        nb_words=50,
        variable_nb_words=True,
    )
    attendance = factory.Faker(
        'random_int',
        min=1,
        max=100,
    )
    training_identifier = factory.Faker('word')
    advertise = factory.Faker(
        'random_element',
        elements=['Y', 'N'],
    )
    # These can probably both use the default:
    # retain_contact = factory.Faker()
    # blogpost = factory.Faker()
    other_requests = factory.Faker(
        'sentence',
        nb_words=50,
        variable_nb_words=True,
    )
    processed = factory.Faker(
        'random_element',
        elements=['UN', 'AP', 'RE'],
    )
