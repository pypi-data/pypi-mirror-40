from django import template


register = template.Library()


@register.simple_tag
def video_thumbnail(video, size=None, extension=None):
    if video:
        width, height = size.split('x')
        return video.get_optimal_conversion_file(width=int(width), height=int(height),
                                                 extension=extension)
    return None
