from __future__ import absolute_import, print_function, unicode_literals

import logging
import os.path
import math
import operator
from decimal import Decimal
from django.apps import apps
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.utils.translation import ugettext_lazy as _
from filer.models.filemodels import File
from filer import settings as filer_settings
from django.utils import six
from easy_thumbnails.files import get_thumbnailer
from django.contrib.staticfiles.templatetags.staticfiles import static
from ..utils.ffmpeg import VideoConverter, UpdatePosterException, VideoMetaException, \
    seconds_to_duration_sting, get_file_meta

from ..settings import FILER_VIDEO_FILE_NAME_EXTENSIONS, FILER_VIDEO_CONVERSION_RESOLUTIONS, \
    FILER_VIDEO_CONVERSION_FORMATS, FILER_VIDEO_CONVERSION_STATUS_PENDING, \
    FILER_VIDEO_CONVERSION_STATUSES, FILER_VIDEO_CONVERSION_STATUS_FAILED, \
    FILER_VIDEO_CONVERSION_STATUS_GENERATING, \
    FILER_VIDEO_POSTER_FROM_FORMAT_RESOLUTION, FILER_VIDEO_CONVERSION_STATUS_DONE, \
    FILER_VIDEO_CONVERSION_STATUS_MANUAL

from ..tasks import run_conversion

logger = logging.getLogger('filer')


class AbstractConversionLog(models.Model):
    time_stamp = models.DateTimeField(null=True, auto_now_add=True)
    conversion = models.ForeignKey(
        'djangocms_filer_video.ConvertedVideoFile',
        related_name='conversion_logs',
        null=True,
    )
    log = models.TextField()

    def __str__(self):
        return '{} | {}'.format(self.time_stamp, self.conversion)

    class Meta:
        abstract = True


class VideoMetaMixin(models.Model):
    meta_width = models.PositiveIntegerField(_('width'), null=True, blank=True, editable=False)
    meta_height = models.PositiveIntegerField(_('height'), null=True, blank=True, editable=False)
    meta_duration_seconds = models.PositiveIntegerField(_('duration'), null=True, blank=True,
                                                        editable=False)
    meta_audio_codec = models.CharField(_('audio codec'), max_length=255, null=True, blank=True, editable=False)
    meta_video_codec = models.CharField(_('video codec'), max_length=255, null=True, blank=True, editable=False)

    def update_meta(self, commit=True):

        try:
            meta = get_file_meta(self.file.path)

            streams = meta['streams']
            video_stream = None
            audio_stream = None
            for stream in streams:
                if stream['codec_type'] == 'video':
                    video_stream = stream
                elif stream['codec_type'] == 'audio':
                    audio_stream = stream

                if video_stream and audio_stream:
                    break

            if video_stream:
                try:
                    self.meta_duration_seconds = int(Decimal(video_stream['duration']))
                except ConversionSyntax as exp:
                    if filer_settings.FILER_ENABLE_LOGGING:
                        logger.error(
                            'Error while fetching meta duration from video file: %s id:%s %s',
                            repr(self), self.pk, exp
                        )
                    if filer_settings.FILER_DEBUG:
                        raise exp
                self.meta_width = int(video_stream['width'])
                self.meta_height = int(video_stream['height'])
                self.meta_video_codec = video_stream.get('codec_name')

            if audio_stream:
                self.meta_audio_codec = audio_stream.get('codec_name')

            if commit:
                self.save()
        except Exception as exp:
            if filer_settings.FILER_ENABLE_LOGGING:
                logger.error(
                    'Error while fetching meta from video file: %s id:%s %s',
                    repr(self), self.pk, exp
                )
            if filer_settings.FILER_DEBUG:
                raise exp

    class Meta:
        abstract = True


class AbstractConvertedVideoFile(VideoMetaMixin):
    video_format = models.CharField(max_length=63, null=True)
    video_resolution = models.CharField(max_length=63, null=True)
    source_video_file = models.ForeignKey(
        'djangocms_filer_video.VideoFile',
        related_name='converted_files',
        null=True,
    )
    file = models.FileField(_('file'), null=True, blank=True)
    status = models.CharField(_('status'), max_length=63, null=True)

    def __str__(self):
        if self.meta_width or self.meta_height:
            resolution = 'x'.join((str(self.meta_width or 0), str(self.meta_height or 0)))
        else:
            resolution = self.video_resolution

        return '{} / {} / {}'.format(
            self.video_format,
            resolution,
            self.status
        )

    def get_format(self):
        for item in FILER_VIDEO_CONVERSION_FORMATS:
            if item.key == self.video_format:
                return item
        return None

    def status_admin_action(self):
        if self.pk is None:
            return ''

        VideoFile = apps.get_model('djangocms_filer_video', 'VideoFile')
        opts = VideoFile._meta

        status_text = FILER_VIDEO_CONVERSION_STATUSES.get(self.status, '')

        if self.status == FILER_VIDEO_CONVERSION_STATUS_FAILED:
            admin_url = reverse_lazy('admin:retry_video_conversion'.format(
                opts.app_label, opts.model_name), kwargs={'conversion_pk': self.pk})
            status_text = ('{} <br><button type="button"'
                           ' onclick="DjangoFilerVideo.retryConversion(this)"'
                           ' data-url="{}">Retry</button>').format(status_text, admin_url)

        elif self.status in [FILER_VIDEO_CONVERSION_STATUS_PENDING,
                             FILER_VIDEO_CONVERSION_STATUS_GENERATING]:
            status_text = '<label data-refresh-url="{0}">{1}</label>'.format(
                reverse_lazy('admin:get_video_conversion_status_action'.format(
                    opts.app_label, opts.model_name), kwargs={'conversion_pk': self.pk}),
                status_text
            )

        return status_text

    def run_conversion(self):
        db_source_video = self.source_video_file
        source_file = db_source_video.file

        out_format = self.get_format()
        out_resolution = self.video_resolution

        with VideoConverter(source_file, out_format, out_resolution) as converter:
            self.status = FILER_VIDEO_CONVERSION_STATUS_GENERATING
            self.save()

            content_file, log_text, exit_code = converter.run()
            self.conversion_logs.create(log=log_text)
            if content_file:
                self.file = content_file
                self.status = FILER_VIDEO_CONVERSION_STATUS_DONE
            if exit_code:
                self.status = FILER_VIDEO_CONVERSION_STATUS_FAILED
            self.save()

        self.update_meta()

    class Meta:
        abstract = True
        unique_together = ('source_video_file', 'video_format', 'video_resolution')
        ordering = ('id',)


class AbstractVideoFile(File, VideoMetaMixin):
    _icon = "video"
    file_type = 'Video'

    poster = models.FileField(_('poster'), null=True, blank=True)

    @classmethod
    def matches_file_type(cls, iname, ifile, request):
        iext = os.path.splitext(iname)[1].lower()
        return iext in FILER_VIDEO_FILE_NAME_EXTENSIONS

    def reset_conversions(self):

        self.converted_files.all().delete()

        conversions = self.create_missing_conversions()

        for conversion in conversions:
            run_conversion.delay(conversion_id=conversion.pk)

    def save(self, *args, **kwargs):
        is_new = (self.pk is None) or kwargs.get('force_insert')
        self.has_all_mandatory_data = self._check_validity()
        super(AbstractVideoFile, self).save(*args, **kwargs)

        if is_new and self.pk and self.has_all_mandatory_data:
            self.update_meta()
            self.update_poster()
            self.reset_conversions()

    def _generate_thumbnails(self, required_thumbnails):
        _thumbnails = {}
        for name, opts in six.iteritems(required_thumbnails):
            try:
                thumb = get_thumbnailer(self.poster).get_thumbnail(opts)
                _thumbnails[name] = thumb.url
            except Exception as exp:
                if filer_settings.FILER_ENABLE_LOGGING:
                    logger.error('Error while generating thumbnail: %s', exp)
                if filer_settings.FILER_DEBUG:
                    raise
        return _thumbnails

    def get_incomplete_conversions(self):
        return self.converted_files.filter(status__in=[
            FILER_VIDEO_CONVERSION_STATUS_PENDING,
            FILER_VIDEO_CONVERSION_STATUS_GENERATING
        ])

    def get_failed_conversions(self):
        return self.converted_files.filter(status__in=[
            FILER_VIDEO_CONVERSION_STATUS_FAILED
        ])

    def get_available_conversions(self):
        return self.converted_files.filter(status__in=[
            FILER_VIDEO_CONVERSION_STATUS_DONE,
            FILER_VIDEO_CONVERSION_STATUS_MANUAL
        ])

    def create_missing_conversions(self):
        new_conversions = set()
        for video_format in FILER_VIDEO_CONVERSION_FORMATS:
            for video_resolution in FILER_VIDEO_CONVERSION_RESOLUTIONS:
                db_conversion, is_new = self.converted_files.get_or_create(
                    video_format=video_format.key,
                    video_resolution=video_resolution,
                )
                if is_new:
                    db_conversion.status = FILER_VIDEO_CONVERSION_STATUS_PENDING
                    db_conversion.save()
                    new_conversions.add(db_conversion)

        return new_conversions

    def static_icons(self, name):
        icon_files = {}
        for size in filer_settings.FILER_ADMIN_ICON_SIZES:
            try:
                icon_files[size] = static(
                    "djangocms_filer_video/icons/{0}_{1}x{2}.png".format(name, size, size)
                )
            except ValueError:
                pass
        return icon_files

    @property
    def icons(self):

        if self.get_incomplete_conversions().exists():
            return self.static_icons('unfinished')
        elif not self.has_all_mandatory_data or self.get_failed_conversions().exists():
            return self.static_icons('failed')
        elif not self.poster:
            return super().icons
        else:
            required_thumbnails = dict(
                (size, {'size': (int(size), int(size)),
                        'crop': True,
                        'upscale': True})
                for size in filer_settings.FILER_ADMIN_ICON_SIZES)
            return self._generate_thumbnails(required_thumbnails)

    def get_poster_format(self):
        for item in FILER_VIDEO_CONVERSION_FORMATS:
            if item.key == FILER_VIDEO_POSTER_FROM_FORMAT_RESOLUTION['format_key']:
                return item
        return None

    def get_poster_resolution(self):
        return FILER_VIDEO_POSTER_FROM_FORMAT_RESOLUTION['resolution']

    def get_duration_sting(self):
        return seconds_to_duration_sting(self.meta_duration_seconds or 0, pretty=True)

    def update_poster(self, seek_to_duration=None):
        source_file = self.file

        out_format = self.get_poster_format()
        out_resolution = self.get_poster_resolution()

        with VideoConverter(source_file, out_format, out_resolution) as converter:
            content_file, log_text, exit_code = converter.run_get_thumbnail(seek_to_duration)
            if content_file:
                self.poster = content_file
                self.save()
            else:
                if filer_settings.FILER_ENABLE_LOGGING:
                    logger.error('Error while generating poster: %s', log_text)
                if filer_settings.FILER_DEBUG:
                    raise UpdatePosterException(log_text)

    def _get_optimal_index(self, iterable, width=None, height=None):
        sizes = [(i, r.meta_width, r.meta_height)
                 for i, r in enumerate(iterable)]
        if width and height:
            distances = (
                (r[0], math.sqrt(math.pow(r[1] - width, 2) + math.pow(r[2] - height, 2)))
                for r in sizes
            )
            return sorted(distances, key=operator.itemgetter(1))[0][0]
        elif width:
            key = 1
            val = width
        else:
            key = 2
            val = height
        distances = (
            (r[0], math.pow(val - r[key], 2)) for r in sizes
        )
        return sorted(distances, key=operator.itemgetter(1))[0][0]

    def get_optimal_conversion_file(self, width=None, height=None, extension=None):
        iterable_qs = self.get_available_conversions()
        if extension:
            filtered_qs = iterable_qs.filter(video_format=extension)
            if filtered_qs.exists():
                iterable_qs = filtered_qs

        filter_kwargs = {}
        if width:
            filter_kwargs.update({'meta_width': width})
        if height:
            filter_kwargs.update({'meta_height': height})

        filtered_qs = iterable_qs.filter(**filter_kwargs)
        matched_resolution_conversion = filtered_qs.first()
        if matched_resolution_conversion:
            return matched_resolution_conversion

        iterable = list(iterable_qs)
        return iterable[self._get_optimal_index(iterable, width, height)] if iterable else None

    def _check_validity(self):
        if not self.matches_file_type(self.original_filename, None, None):
            return False
        return True

    class Meta(object):
        app_label = 'djangocms_filer_video'
        verbose_name = _('video')
        verbose_name_plural = _('videos')
        abstract = True
