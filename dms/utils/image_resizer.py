from imagekit import ImageSpec
from pilkit.processors import ResizeToFit


class ImageResizer(ImageSpec):
    processors = [ResizeToFit(150, None, False)]
    format = 'JPEG'
    options = {'quality': 100}
