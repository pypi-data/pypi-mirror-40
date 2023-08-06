# -*- coding: utf-8 -*-
from __future__ import absolute_import

import subprocess as sp
import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

from .utils.compat import DEVNULL
from .utils.video_formats import VideoFormat

logger = logging.getLogger('filer')

FILER_VIDEO_FILE_NAME_EXTENSIONS = getattr(settings,
                                           'FILER_VIDEO_FILE_NAME_EXTENSIONS',
                                           ['.dv', '.mov', '.mp4', '.avi', '.wmv'])

FILER_VIDEO_DEFAULT_FOLDER = getattr(settings,
                                     'FILER_VIDEO_DEFAULT_FOLDER',
                                     'Videos')

FILER_VIDEO_CONVERSION_FORMATS = getattr(settings,
                                         'FILER_VIDEO_CONVERSION_FORMATS',
                                         [
                                             VideoFormat('mp4', _('MP4'), [
                                                 '-codec:v', 'libx264',
                                                 '-preset', 'slow',
                                                 '-crf', '24',
                                                 '-codec:a', 'aac',
                                                 '-flags', '+global_header',
                                                 '-strict', 'experimental'
                                             ]),
                                             VideoFormat('webm', _('WebM'), [
                                                 '-codec:v', 'libvpx',
                                                 '-crf', '22',
                                                 '-codec:a', 'libvorbis',
                                             ]),
                                         ])

FILER_VIDEO_CONVERSION_RESOLUTIONS = getattr(settings,
                                             'FILER_VIDEO_CONVERSION_RESOLUTIONS',
                                             ('1280x-1', '640x-1'))


def _first_format_resolution():
    return {
        'format_key': FILER_VIDEO_CONVERSION_FORMATS[0].key,
        'resolution': FILER_VIDEO_CONVERSION_RESOLUTIONS[0],
    }

FILER_VIDEO_POSTER_FROM_FORMAT_RESOLUTION = getattr(
    settings, 'FILER_VIDEO_POSTER_FROM_FORMAT_RESOLUTION',
    _first_format_resolution()
)


FILER_VIDEO_CONVERSION_STATUS_DONE = getattr(settings,
                                             'FILER_VIDEO_CONVERSION_STATUS_DONE',
                                             'Done')

FILER_VIDEO_CONVERSION_STATUS_MANUAL = getattr(settings,
                                               'FILER_VIDEO_CONVERSION_STATUS_MANUAL',
                                               'Manual')

FILER_VIDEO_CONVERSION_STATUS_PENDING = getattr(settings,
                                                'FILER_VIDEO_CONVERSION_STATUS_PENDING',
                                                'Pending')

FILER_VIDEO_CONVERSION_STATUS_GENERATING = getattr(settings,
                                                   'FILER_VIDEO_CONVERSION_STATUS_GENERATING',
                                                   'Generating')

FILER_VIDEO_CONVERSION_STATUS_FAILED = getattr(settings,
                                               'FILER_VIDEO_CONVERSION_STATUS_FAILED',
                                               'Failed')

FILER_VIDEO_CONVERSION_STATUSES = getattr(
    settings,
    'FILER_VIDEO_CONVERSION_STATUS',
    {
        None: _('Unknown'),
        FILER_VIDEO_CONVERSION_STATUS_DONE: _('Done'),
        FILER_VIDEO_CONVERSION_STATUS_MANUAL: _('Manually uploaded'),
        FILER_VIDEO_CONVERSION_STATUS_PENDING: _('Pending'),
        FILER_VIDEO_CONVERSION_STATUS_GENERATING: _('Generating'),
        FILER_VIDEO_CONVERSION_STATUS_FAILED: _('Failed'),
    }
)


def _try_cmd(cmd):
    try:
        popen_params = {
            "stdout": sp.PIPE,
            "stderr": sp.PIPE,
            "stdin": DEVNULL
        }

        process = sp.Popen(cmd, **popen_params)
        process.communicate()
    except Exception as exp:
        return False, exp
    else:
        return True, None


FILER_VIDEO_FFMPEG_BINARY = getattr(settings, 'FILER_VIDEO_FFMPEG_BINARY', 'auto-detect')
FILER_VIDEO_FFPROBE_BINARY = getattr(settings, 'FILER_VIDEO_FFPROBE_BINARY', 'auto-detect')

if FILER_VIDEO_FFMPEG_BINARY == 'auto-detect':
    if _try_cmd(['ffmpeg'])[0]:
        FILER_VIDEO_FFMPEG_BINARY = 'ffmpeg'
        FILER_VIDEO_FFPROBE_BINARY = 'ffprobe'
    elif _try_cmd(['avconv'])[0]:
        FILER_VIDEO_FFMPEG_BINARY = 'avconv'
        FILER_VIDEO_FFPROBE_BINARY = 'avprobe'
    elif _try_cmd(['ffmpeg.exe'])[0]:
        FILER_VIDEO_FFMPEG_BINARY = 'ffmpeg.exe'
        FILER_VIDEO_FFPROBE_BINARY = 'avprobe.exe'
    else:
        FILER_VIDEO_FFMPEG_BINARY = 'unset'
        FILER_VIDEO_FFPROBE_BINARY = 'unset'
        logging.error("Django-filer-video: can't auto detect ffmpeg binary")
else:
    success, err = _try_cmd([FILER_VIDEO_FFMPEG_BINARY])
    if not success:
        raise ImproperlyConfigured(
            str(err) +
            " - The path specified for the ffmpeg binary might be wrong")




