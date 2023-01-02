"""Seed the database with dummy test data."""

from datetime import date, timedelta
from django.db import transaction
from django.core.management.base import BaseCommand

from training.models import Training
from training.factories import TrainingFactory

DEFAULT_EVENTS = 50
DEFAULT_START_DAYS = 0
DEFAULT_END_DAYS = 180


class Command(BaseCommand):
    """Seed the database."""

    help = (
        "Generate fake training events for testing.\n"
        "WARNING: This will delete all database content!"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "-n",
            type=int,
            default=DEFAULT_EVENTS,
            required=False,
            help=f"Number of records to create (default {DEFAULT_EVENTS})",
        )
        parser.add_argument(
            "-s",
            type=int,
            required=False,
            default=DEFAULT_START_DAYS,
            help=(
                "Days from today when events will start"
                f" (default {DEFAULT_START_DAYS} days)."
            ),
        )
        parser.add_argument(
            "-e",
            type=int,
            default=DEFAULT_END_DAYS,
            required=False,
            help=(
                "Days from today when events will end"
                f" (default {DEFAULT_END_DAYS} days)."
            ),
        )

    @transaction.atomic
    def handle(self, *args, **kwargs):
        """Run the command."""
        input(
            "\nWARNING: This will delete all database content!\n\n"
            "Press ENTER to continue or CTRL+C to cancel."
        )

        n = kwargs["n"]
        self.stdout.write("\nDeleting existing Training events...")
        Training.objects.all().delete()

        dt_start = date.today() + timedelta(days=kwargs["s"])
        dt_end = date.today() + timedelta(days=kwargs["e"])
        self.stdout.write(
            f"\nPopulating database with {n} records...\n"
            f"Start date: {dt_start.strftime('%d-%m-%Y')}"
            f"   (+{kwargs['s']} days)\n"
            f"End date:   {dt_end.strftime('%d-%m-%Y')}"
            f"   (+{kwargs['e']} days)"
        )

        for _ in range(n):
            TrainingFactory(
                start_min_days=kwargs["s"], start_max_days=kwargs["e"],
            )
