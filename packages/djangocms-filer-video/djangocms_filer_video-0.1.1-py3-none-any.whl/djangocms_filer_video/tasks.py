# coding: utf-8
from celery import task, Task
from django.core.management import call_command
import logging

logger = logging.getLogger('filer')


class DjangoFilerVideoTask(Task):
    max_retries = 3

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error('djangocms_filer_video task failed: task_id: {}, args: {}, kwargs: {}'.format(
            task_id, args, kwargs))


@task(base=DjangoFilerVideoTask)
def run_conversion(*args, **kwargs):
    conversion_id = int(kwargs['conversion_id'])
    call_command('run_conversion', conversion_id=conversion_id)


@task(base=DjangoFilerVideoTask)
def update_poster(*args, **kwargs):
    video_file_id = int(kwargs['video_file_id'])
    seek_to_duration = int(kwargs.get('seek_to_duration')) or None
    call_command(
        'update_poster',
        conversion_id=video_file_id,
        seek_to_duration=seek_to_duration
    )
