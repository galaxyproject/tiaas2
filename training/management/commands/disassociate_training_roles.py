from django.core.management.base import BaseCommand, CommandError
from django.db.utils import ProgrammingError
import datetime
from training.models import Training
from training.galaxy import (
    disassociate_role,
    execute_txn
)


class Command(BaseCommand):
    help = 'Removes users from all expired trainings'

    def add_arguments(self, parser):
        parser.add_argument('--commit', action='store_true')

    def handle(self, commit, *args, **options):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        for event in Training.objects.filter(end__lte=yesterday):
            print(f"Removing users from {event}")
            try:
                print(disassociate_role(event.training_identifier, commit=commit))
            except ProgrammingError as pe:
                print(pe)
