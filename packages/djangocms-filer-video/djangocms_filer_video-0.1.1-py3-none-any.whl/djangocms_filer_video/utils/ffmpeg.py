import os
import shutil
import subprocess
import tempfile
import re
import json

from django.core.files.base import ContentFile
from django.utils.text import slugify

from .compat import DEVNULL
from ..settings import FILER_VIDEO_FFMPEG_BINARY, FILER_VIDEO_FFPROBE_BINARY
from datetime import timedelta


class UpdatePosterException(Exception):
    pass


class VideoMetaException(Exception):
    pass


def seconds_to_duration_sting(in_seconds, pretty=False):
    hour = int(in_seconds // 3600)
    minute = int((in_seconds % 3600) // 60)
    second = int((in_seconds % 3600) % 60)
    if not pretty:
        return '{}:{}:{}'.format(hour, minute, second)

    return ':'.join(
        str(item).zfill(2)
        for idx, item in enumerate((hour, minute, second))
        if item or idx
    )


def get_file_meta(in_file_path):
    try:
        popen_params = {
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "stdin": DEVNULL
        }

        base_args = (FILER_VIDEO_FFPROBE_BINARY, '-of', 'json', '-show_format', '-show_streams')

        args = base_args + (in_file_path,)
        proc = subprocess.Popen(args, **popen_params)
        out, log = proc.communicate()
        out_text = out.decode('utf8')
        out_log = log.decode('utf8')
        proc.stderr.close()
        meta = json.loads(out_text)
        if not meta:
            raise VideoMetaException(out_log or 'Video meta is empty')
    except Exception as exp:
        raise exp

    return meta


class VideoConverter:
    in_file = None
    in_filename = None
    in_file_path = None

    out_format = None
    out_dir = None
    out_filename = None
    out_thumbnail_filename = 'thumbnail.png'
    out_file_path = None
    out_thumbnail_path = None
    out_resolution = None

    base_args = (FILER_VIDEO_FFMPEG_BINARY, '-i')

    def get_scale_string(self):
        return ':'.join(str(int(item)) for item in self.out_resolution.split('x'))

    def get_scale_args(self):
        return '-vf', 'scale={0}'.format(self.get_scale_string())

    def get_ffmpeg_args(self, exit_on_error=True):
        args = (self.base_args +
                (self.in_file_path,) +
                tuple(self.out_format.ffmpeg_args) +
                tuple(self.get_scale_args()))
        if exit_on_error:
            args += ('-xerror',)
        args += (self.out_file_path,)
        return args

    def run(self):
        try:
            args = self.get_ffmpeg_args()
            popen_params = {
                "stdout": DEVNULL,
                "stderr": subprocess.PIPE,
                "stdin": DEVNULL
            }

            proc = subprocess.Popen(args, **popen_params)

            out, log = proc.communicate()
            proc.stderr.close()
            log_text = log.decode('utf8')

            return (ContentFile(open(self.out_file_path, 'rb').read(), self.out_filename),
                    log_text,
                    proc.returncode)
        except Exception as error:
            log_text = getattr(error, 'output', str(error))
            return None, log_text, 1

    def get_file_duration(self):
        popen_params = {
            "stdout": DEVNULL,
            "stderr": subprocess.PIPE,
            "stdin": DEVNULL
        }

        args = self.base_args + (self.in_file_path,)
        proc = subprocess.Popen(args, **popen_params)
        out, log = proc.communicate()
        log_text = log.decode('utf8')
        proc.stderr.close()
        matches = re.search(
            r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),",
            log_text,
            re.DOTALL
        )
        if not matches:
            raise VideoMetaException(log_text)

        matches = matches.groupdict()

        total_duration = timedelta(hours=int(matches.get('hours', 0)),
                                   minutes=int(matches.get('minutes', 0)),
                                   seconds=int(float(matches.get('seconds', 0))))

        return total_duration

    def run_get_thumbnail(self, seek_to_duration=None):
        try:
            popen_params = {
                "stdout": DEVNULL,
                "stderr": subprocess.PIPE,
                "stdin": DEVNULL
            }

            if not seek_to_duration:
                total_duration = self.get_file_duration()
                seek_to_duration = total_duration.total_seconds() / 3

            seek_to_duration_arg = seconds_to_duration_sting(seek_to_duration)

            args = (
                self.base_args +
                (self.in_file_path,) +
                ('-ss', seek_to_duration_arg, '-vframes', '1',) +
                tuple(self.get_scale_args()) +
                (self.out_thumbnail_path,)
            )
            proc = subprocess.Popen(args, **popen_params)
            out, log = proc.communicate()
            proc.stderr.close()
            log_text = log.decode('utf8')

            return (
                ContentFile(
                    open(self.out_thumbnail_path, 'rb').read(), self.out_thumbnail_filename
                ),
                log_text,
                proc.returncode
            )
        except Exception as error:
            log_text = getattr(error, 'output', str(error))
            return None, log_text, 1

    def __init__(self, in_file, out_format, out_resolution):

        self.in_file = in_file
        self.out_format = out_format
        self.out_resolution = out_resolution

        self.in_file_path = self.in_file.path
        self.in_filename = os.path.splitext(os.path.basename(self.in_file.name))[0]

        self.validate_path(self.in_file_path)

    def validate_path(self, path):
        if '..' in path:
            raise ValueError('Relative path is unavailable for security reasons')

    def init_temp(self):
        self.out_dir = tempfile.mkdtemp()
        self.out_filename = "{0}_{1}.{2}".format(
            slugify(self.in_filename),
            slugify(self.get_scale_string()),
            self.out_format.key
        )
        self.out_file_path = os.path.join(self.out_dir, self.out_filename)

        self.out_thumbnail_path = os.path.join(self.out_dir, self.out_thumbnail_filename)
        try:
            self.validate_path(self.out_file_path)
        except ValueError as exp:
            self.clean_temp()
            raise exp

    def clean_temp(self):
        shutil.rmtree(self.out_dir, ignore_errors=True)

    def __enter__(self):
        self.init_temp()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.clean_temp()
