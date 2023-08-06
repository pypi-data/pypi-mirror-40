from .abstract_models import AbstractVideoFile, AbstractConvertedVideoFile, AbstractConversionLog


class ConversionLog(AbstractConversionLog):
    pass


class ConvertedVideoFile(AbstractConvertedVideoFile):
    pass


class VideoFile(AbstractVideoFile):
    pass
