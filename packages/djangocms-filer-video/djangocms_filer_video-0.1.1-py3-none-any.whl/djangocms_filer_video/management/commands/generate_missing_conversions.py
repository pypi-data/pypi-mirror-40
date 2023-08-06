from django.core.management.base import BaseCommand
from django.db import transaction
from ...models import VideoFile
from ...tasks import run_conversion


class Command(BaseCommand):
    help = 'Find missing conversions and delay run celery "run_conversion" tasks'

    def handle(self, *args, **options):
        missing_conversions_ids = set()
        videos_ids_with_missing_conversions = set()

        with transaction.atomic():
            for db_video in VideoFile.objects.all():
                conversions = db_video.create_missing_conversions()
                for conversion in conversions:
                    missing_conversions_ids.add(conversion.pk)
                    videos_ids_with_missing_conversions.add(db_video.pk)

        for conversion_id in missing_conversions_ids:
            run_conversion.delay(conversion_id=conversion_id)

        print('Generated {} new conversions for {} video files'.format(
            len(missing_conversions_ids), len(videos_ids_with_missing_conversions)
        ))
