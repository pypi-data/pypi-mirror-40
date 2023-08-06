import unittest
import os
from ybc_image import *
from ybc_exception import *


class TestYbcImage(unittest.TestCase):
    path_pic = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'test.jpg')

    def test_addtext(self):
        self.assertIsNotNone(addtext(self.path_pic, "你好"))

    def test_addtext_exType(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用addtext方法时，'image'、'text'、'location'参数类型错误。$"):
            addtext(1, 1, 1)

    def test_addtext_exValue(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用addtext方法时，'image'、'location'参数不在允许范围内。$"):
            addtext('111', '111', '111')

    def test_addtext_textlen_ex(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用addtext方法时，'text'参数不在允许范围内。$"):
            addtext(self.path_pic, "123456789987654321")


if __name__ == '__main__':
    unittest.main()
