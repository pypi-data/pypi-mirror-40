from django.core.management.base import BaseCommand

from ...models import ConvertedVideoFile
from ...tasks import run_conversion
from ...settings import FILER_VIDEO_CONVERSION_STATUS_DONE, \
    FILER_VIDEO_CONVERSION_STATUS_MANUAL, FILER_VIDEO_CONVERSION_STATUS_FAILED


class Command(BaseCommand):
    help = 'Finds conversions with specialized status ' \
           '(if specified else - not finished conversions) ' \
           'and puts them in a "run_conversion" task queue'

    def add_arguments(self, parser):

        parser.add_argument(
            '--status', action='store', dest='status', type=str,
            default=None
        )

    def handle(self, *args, **options):
        status = options.get('status')
        if status:
            db_conversion_qs = ConvertedVideoFile.objects.filter(status=status)
        else:
            complete_statuses = [
                FILER_VIDEO_CONVERSION_STATUS_DONE, FILER_VIDEO_CONVERSION_STATUS_MANUAL,
                FILER_VIDEO_CONVERSION_STATUS_FAILED
            ]
            db_conversion_qs = ConvertedVideoFile.objects.exclude(status__in=complete_statuses)

        for db_conversion in db_conversion_qs:
            run_conversion.delay(conversion_id=db_conversion.pk)
