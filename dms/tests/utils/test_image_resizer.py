from PIL import Image
from dms.tests.base import MongoTestCase
from dms.utils import image_resizer
from necoc import settings


class ImageResizerTest(MongoTestCase):

    def test_resizes_by_width_to_150(self):
        image = open(settings.PROJECT_ROOT + '/../dms/tests/large_test.jpg', 'rb')
        resized_image = image_resizer.ImageResizer(image).generate()
        width, height = Image.open(resized_image).size
        self.assertEqual(150, width)
        self.assertEqual(93, height)