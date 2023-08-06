"""
Video extension for Django filer.
"""

VERSION = (0, 1, 1, 'dev')


def get_release():
    return '-'.join([get_version(), VERSION[-1]])


def get_version():
    """
    Returns only digit parts of version.
    """
    return '.'.join(str(i) for i in VERSION[:3])


__version__ = get_release()

default_app_config = 'djangocms_filer_video.apps.FilerVideoConfig'
