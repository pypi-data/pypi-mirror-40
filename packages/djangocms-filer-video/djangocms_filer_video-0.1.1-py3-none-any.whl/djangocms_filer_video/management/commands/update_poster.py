from django.core.management.base import BaseCommand
from ...models import VideoFile


class Command(BaseCommand):
    help = 'Update poster'

    def add_arguments(self, parser):

        parser.add_argument(
            '--video_file_id', action='store', dest='video_file_id', type=int,
            default=None
        )
        parser.add_argument(
            '--seek_to_duration', action='store', dest='seek_to_duration', type=int,
            default=None
        )

    def handle(self, *args, **options):
        video_file_id = options['video_file_id']
        seek_to_duration = options.get('seek_to_duration')

        db_source_video = VideoFile.objects.get(pk=video_file_id)
        db_source_video.update_poster(seek_to_duration)
