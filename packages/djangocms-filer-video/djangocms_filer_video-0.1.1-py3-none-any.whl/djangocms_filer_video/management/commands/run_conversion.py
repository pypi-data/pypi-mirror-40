from django.core.management.base import BaseCommand

from ...models import ConvertedVideoFile


class Command(BaseCommand):
    help = 'Run conversion'

    def add_arguments(self, parser):

        parser.add_argument(
            '--conversion_id', action='store', dest='conversion_id', type=int,
            default=None
        )

    def handle(self, *args, **options):
        db_conversion = ConvertedVideoFile.objects.get(pk=options['conversion_id'])
        db_conversion.run_conversion()
