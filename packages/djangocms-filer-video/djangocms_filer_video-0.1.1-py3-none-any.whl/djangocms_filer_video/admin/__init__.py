# -*- coding: utf-8 -*-

from django.contrib import admin

from .videoadmin import VideoFileAdmin, ConversionLogAdmin
from ..models import VideoFile, ConversionLog

admin.site.register(VideoFile, VideoFileAdmin)
admin.site.register(ConversionLog, ConversionLogAdmin)
