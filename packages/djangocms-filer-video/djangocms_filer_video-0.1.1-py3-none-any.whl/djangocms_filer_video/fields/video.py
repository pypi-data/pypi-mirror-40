# -*- coding: utf-8 -*-
from __future__ import absolute_import

from ..models import VideoFile
from filer.fields.file import AdminFileFormField, AdminFileWidget, FilerFileField
from filer.models.foldermodels import Folder
from django.core.urlresolvers import reverse_lazy
from ..settings import FILER_VIDEO_DEFAULT_FOLDER


class AdminVideoFileWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        attrs = attrs or {}
        attrs['class'] = 'vForeignKeyRawIdAdminField adminVideoFileWidget'

        video_folder = Folder.objects.filter(
            parent__isnull=True, name=FILER_VIDEO_DEFAULT_FOLDER).first()
        if video_folder:
            upload_url = reverse_lazy(
                'admin:filer-ajax_upload', kwargs={'folder_id': video_folder.pk}
            )
            attrs['data-default-upload-url'] = upload_url
        return super().render(name, value, attrs)

    class Media(AdminFileWidget.Media):
        js = AdminFileWidget.Media.js + (
            'djangocms_filer_video/video_file_field.js',
        )


class AdminVideoFileFormField(AdminFileFormField):
    widget = AdminVideoFileWidget


class FilerVideoFileField(FilerFileField):
    default_form_class = AdminVideoFileFormField
    default_model_class = VideoFile
