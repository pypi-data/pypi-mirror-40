# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.conf.urls import url
from django.contrib.admin import TabularInline, ModelAdmin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.utils.translation import ugettext as _
from filer.admin.fileadmin import FileAdmin
from filer.settings import FILER_ENABLE_PERMISSIONS

from .forms import VideoFileAdminForm, ConvertedVideoFileForm
from ..models import ConvertedVideoFile, ConversionLog
from ..settings import (
    FILER_VIDEO_CONVERSION_STATUS_FAILED,
    FILER_VIDEO_CONVERSION_STATUS_PENDING
)
from ..tasks import run_conversion


class ConvertedVideoFileInline(TabularInline):
    model = ConvertedVideoFile
    form = ConvertedVideoFileForm
    can_delete = False
    readonly_fields = ['status_action', 'logs']
    fieldsets = (
        (None, {'fields': ('file', 'video_format', 'video_resolution', 'status_action', 'logs')}),
    )
    extra = 1

    def status_action(self, obj):
        return obj.status_admin_action()

    def logs(self, obj):
        if obj.pk is None:
            return ''

        opts = ConversionLog._meta
        admin_url = reverse_lazy('admin:{0}_{1}_changelist'.format(
            opts.app_label, opts.model_name))

        return '<a href="{}?conversion_id={}" target="_blank">Show Logs</a>'.format(
            admin_url, obj.pk
        )

    logs.short_description = _('Logs')
    logs.allow_tags = True

    status_action.short_description = _('Status')
    status_action.allow_tags = True


class ConversionLogAdmin(ModelAdmin):
    list_display = ['time_stamp', 'conversion', ]
    exclude = ['conversion']

    def has_module_permission(self, request):
        return False


class VideoFileAdmin(FileAdmin):
    form = VideoFileAdminForm
    inlines = [ConvertedVideoFileInline]
    readonly_fields = ('duration_time',) + FileAdmin.readonly_fields

    def has_module_permission(self, request):
        return False

    @classmethod
    def build_fieldsets(cls, extra_main_fields=(), extra_advanced_fields=(),
                        extra_fieldsets=()):
        fieldsets = (
            (None, {
                'fields': ('poster',
                           'duration_time',
                           'name',
                           'owner',
                           'description',
                           ) + extra_main_fields,
            }),
        )
        if extra_advanced_fields:
            fieldsets += (
                (_('Advanced'), {
                    'fields': extra_advanced_fields,
                    'classes': ('collapse',),
                }),
            )

        fieldsets += (
            (_('Hidden'), {
                'fields': ('file',
                           'sha1',
                           'display_canonical',),
                'classes': ('hidden',),
            }),
        )

        fieldsets += extra_fieldsets

        if FILER_ENABLE_PERMISSIONS:
            fieldsets = fieldsets + (
                (None, {
                    'fields': ('is_public',)
                }),
            )
        return fieldsets

    def duration_time(self, obj):
        return obj.get_duration_sting()

    duration_time.short_description = _('Duration time')

    def get_urls(self):
        urls = super(VideoFileAdmin, self).get_urls()
        my_urls = [
            url(r'^retry_video_conversion/(?P<conversion_pk>\d+?)/$',
                self.admin_site.admin_view(self.retry_conversion),
                name='retry_video_conversion'),
            url(r'^get_video_conversion_status_action/(?P<conversion_pk>\d+?)/$',
                self.admin_site.admin_view(self.get_conversion_status_action),
                name='get_video_conversion_status_action'),
        ]
        return my_urls + urls

    def get_conversion_status_action(self, request, conversion_pk):
        if request.is_ajax():
            db_conversion = ConvertedVideoFile.objects.get(
                pk=conversion_pk
            )

            return JsonResponse(
                {
                    'conversion_pk': db_conversion.pk,
                    'status_admin_action': db_conversion.status_admin_action()
                }
            )
        return HttpResponseBadRequest()

    def retry_conversion(self, request, conversion_pk):
        if request.is_ajax():
            db_conversion = ConvertedVideoFile.objects.get(
                pk=conversion_pk
            )
            if db_conversion.status == FILER_VIDEO_CONVERSION_STATUS_FAILED:
                db_conversion.status = FILER_VIDEO_CONVERSION_STATUS_PENDING
                db_conversion.save()
                run_conversion.delay(conversion_id=db_conversion.pk)

            return JsonResponse(
                {
                    'conversion_pk': db_conversion.pk,
                    'status': db_conversion.status_admin_action()
                }
            )
        return HttpResponseBadRequest()


VideoFileAdmin.fieldsets = VideoFileAdmin.build_fieldsets()
