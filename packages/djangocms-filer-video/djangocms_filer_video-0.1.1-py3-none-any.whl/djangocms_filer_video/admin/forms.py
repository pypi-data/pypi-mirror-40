# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django import forms

from ..models.video_models import VideoFile
from ..settings import (
    FILER_VIDEO_CONVERSION_RESOLUTIONS, FILER_VIDEO_CONVERSION_FORMATS,
    FILER_VIDEO_CONVERSION_STATUS_MANUAL
)


class ConvertedVideoFileForm(forms.ModelForm):
    EMPTY_CHOICES = [(None, '')]

    video_format = forms.ChoiceField(
        required=True,
        choices=EMPTY_CHOICES + [
            (item.key, item.name)
            for item in sorted(FILER_VIDEO_CONVERSION_FORMATS, key=lambda x: x.name)
        ]
    )
    video_resolution = forms.ChoiceField(
        required=True,
        choices=EMPTY_CHOICES + [(item, item)
                                 for item in sorted(FILER_VIDEO_CONVERSION_RESOLUTIONS)]
    )

    def save(self, commit=True):
        if 'file' in self.changed_data:
            self.cleaned_data['status'] = FILER_VIDEO_CONVERSION_STATUS_MANUAL
            self.instance.status = self.cleaned_data['status']
        instance = super().save(commit)
        if commit and 'file' in self.changed_data:
            instance.update_meta(False)
        return instance


class VideoFileAdminForm(forms.ModelForm):
    class Meta(object):
        model = VideoFile
        fields = '__all__'

    class Media(object):
        js = (
            'djangocms_filer_video/admin_form.js',
        )
