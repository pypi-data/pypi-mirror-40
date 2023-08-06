from django.core.management.base import BaseCommand
from ...models import VideoFile


class Command(BaseCommand):
    help = 'Update meta data'

    def add_arguments(self, parser):

        parser.add_argument(
            '--video_file_id', action='store', dest='video_file_id', type=int,
            default=None
        )

    def handle(self, *args, **options):
        video_file_id = options.get('video_file_id')
        filter_kwargs = {}
        if video_file_id is not None:
            filter_kwargs['id'] = video_file_id

        for db_source_video in VideoFile.objects.filter(**filter_kwargs):
            db_source_video.update_meta()
            for db_conversion in db_source_video.converted_files.all():
                db_conversion.update_meta()
