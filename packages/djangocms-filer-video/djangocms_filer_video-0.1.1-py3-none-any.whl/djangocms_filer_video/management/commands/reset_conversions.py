from django.core.management.base import BaseCommand

from ...models import VideoFile


class Command(BaseCommand):
    help = 'Clears and regenerates conversions for specified video file'

    def add_arguments(self, parser):

        parser.add_argument(
            '--video_file_id', action='store', dest='video_file_id', type=int,
            default=None
        )

    def handle(self, *args, **options):
        video_file_id = options['video_file_id']

        db_source_video = VideoFile.objects.get(pk=video_file_id)
        db_source_video.reset_conversions()
