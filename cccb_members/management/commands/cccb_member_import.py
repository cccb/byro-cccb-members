
"""
CCCB Member import
"""

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Import CCCB members from CSV"

    def add_arguments(self, parser):
        """Add cli flags"""
        parser.add_argument(
            "-f", "--filename",
            required=True,
            help="The CSV member list export")

    def handle(self, *args, **options):
        """Import members from CSV list"""

        print("Importing member from: {}".format(
            options["filename"]))

