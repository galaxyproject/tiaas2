"""Seed the database with dummy test data."""

from django.db import transaction
from django.core.management.base import BaseCommand

from training.models import Training
from training.factories import TrainingFactory

NUM_TRAININGS = 40


class Command(BaseCommand):
    """Seed the database."""

    help = (
        "Generate 8 random training instances.\n"
        "WARNING: This will delete all database content!")

    @transaction.atomic
    def handle(self, *args, **kwargs):
        """Run the command."""
        input(
            "\nWARNING: This will delete all database content!\n\n"
            'Press ENTER to continue or CTRL+C to cancel.')

        self.stdout.write("Deleting old data...")
        Training.objects.all().delete()

        self.stdout.write("Creating new data...")

        for _ in range(NUM_TRAININGS):
            TrainingFactory()
