class VideoFormat(object):
    key = None
    name = None
    ffmpeg_args = None

    def __init__(self, key, name, ffmpeg_args):
        super().__init__()
        self.key = key
        self.name = name
        self.ffmpeg_args = ffmpeg_args
