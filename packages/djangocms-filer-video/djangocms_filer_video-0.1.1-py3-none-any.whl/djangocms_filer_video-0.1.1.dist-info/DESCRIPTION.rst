djangocms-filer-video
==================

Video extension for Django filer.

.. image:: https://travis-ci.org/Air-Mark/djangocms-filer-video.svg?branch=master
    :target: https://travis-ci.org/Air-Mark/djangocms-filer-video
.. image:: https://coveralls.io/repos/Air-Mark/djangocms-filer-video/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/Air-Mark/djangocms-filer-video?branch=master


Quick start
************

#. Install ``djangocms-filer-video``:

   ::

      pip install djangocms-filer-video


   or from sources

   ::

      pip install git+https://github.com/Air-Mark/djangocms-filer-video.git


#. Add ``djangocms_filer_video`` to ``INSTALLED_APPS`` in your Django settings.

#. Add video field to filer settings into settings file. Note: the order is important.

   ::

      FILER_FILE_MODELS = (
            'filer.Image',
            'djangocms_filer_video.VideoFile',
            'filer.File',
      )


#. Usage of template tags:

   ::

        {% load filer_video_tags %}
        {% video_thumbnail video '1280x0' 'mp4' as video_large_mp4 %}
        {% video_thumbnail video '640x0' 'mp4' as video_small_mp4 %}
        <div class="product__video-in">
            <video style="width: 50%" loop="loop" data-width="{{ video_small_mp4.meta_width }}" data-height="{{ video_small_mp4.meta_height }}" muted="muted" poster="{{ poster }}">
                <source src="{{ video_small_mp4.file.url }}" data-large="{{ video_large_mp4.file.url }}" type="video/{{ video_small_mp4.video_format }}">
            </video>
        </div>

#. Usage of model fields

   ::

      from django.db import models
      from djangocms_filer_video.fields.video import FilerVideoFileField


      class ExampleModel(models.Model):
         main_video = FilerVideoFileField(verbose_name=_('Main video'), blank=True, null=True,
                                          on_delete=models.SET_NULL,
                                          related_name='post_properties_video')


Release 0.1 (Januar 17, 2019)
--------------------------

- Initial release

