import sys
from PIL import Image, ImageDraw, ImageFont
from ybc_exception import *


def addtext(image='', text='', location='top'):
    """
    图片加文字
    :参数 image: 需要添加文字的图片路径
    :参数 text: 待添加的文字
    :参数 location: 支持的值为 ['top', 'center', 'bottom']
    :返回值: PIL.image 对象
    """
    err_msg = str()
    err_flag = False
    if not isinstance(image, str):
        err_msg = "'image'"
        err_flag = True
    if not isinstance(text, str):
        if err_flag:
            err_msg += "、'text'"
        else:
            err_msg = "'text'"
            err_flag = True
    if not isinstance(location, str):
        if err_flag:
            err_msg += "、'location'"
        else:
            err_msg = "'location'"
            err_flag = True
    if err_flag:
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg=err_msg)

    if not(('.' in image) and (image.split('.')[-1].lower() in ['png', 'jpg', 'jpeg'])):
        err_msg = "'image'"
        err_flag = True
    if location not in ['top', 'center', 'bottom']:
        if err_flag:
            err_msg += "、'location'"
        else:
            err_msg = "'location'"
            err_flag = True
    if err_flag:
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg=err_msg)

    if len(text) > 15:
        sys.stdout.write('最多支持输入15个中文字符\n')
        sys.stdout.flush()
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg="'text'")

    try:
        def get_suitable_ttf(img_width, input_text):
            """
            get the suitable FreeTypeFont object to add on the image
            :param img_width: the image's width
            :param input_text: the text need to add on
            :return: the FreeTypeFont object
            """
            DEFAULT_FONT = 'NotoSansCJK-Bold.ttc'
            DEFAULT_FONT_SIZE = 24

            # if the font hasn't been installed, we print the tip first
            try:
                ttf = ImageFont.truetype(DEFAULT_FONT, DEFAULT_FONT_SIZE)
            except Exception as e:
                print("ybc_image 的正常运行需要 NotoSansCJK-Bold.ttc 字体，请安装对应字体后重试")
                sys.stdout.flush()
                raise e

            text_width = ttf.getsize(input_text)[0]
            # if text's width less than image's width, add on directly
            if text_width <= img_width:
                return ttf
            # if text's width larger than image's width, we need to calculate the suitable font size
            else:
                font_size_max = DEFAULT_FONT_SIZE
                font_size_min = 1

                # stop when (min == max) or (min == max - 1)
                while font_size_min < font_size_max - 1:
                    font_size = (font_size_min + font_size_max) // 2
                    text_width = ImageFont.truetype(DEFAULT_FONT, font_size).getsize(input_text)[0]

                    if text_width < img_width:
                        font_size_min = font_size
                    elif text_width > img_width:
                        font_size_max = font_size
                    else:
                        break

                # use the size_min to ensure the text_width < image_width
                return ImageFont.truetype(DEFAULT_FONT, font_size_min)

        img_bg = Image.open(image)
        font = get_suitable_ttf(img_bg.size[0], text)
        text_info = font.getsize(text)
        draw = ImageDraw.Draw(img_bg)
        text_loc = int()
        if location == "bottom":
            text_loc = img_bg.size[1] - text_info[1]
        elif location == "center":
            text_loc = (img_bg.size[1] - text_info[1]) // 2
        elif location == "top":
            text_loc = 0
        draw.text(((img_bg.size[0] - text_info[0]) // 2, text_loc), text, fill=(0, 0, 0), font=font)
        return img_bg

    except Exception as e:
        raise InternalError(e, 'ybc_image')


def main():
    addtext('test.jPG', '你好呀呀呀').show()
    # addtext('test.jpg', '1你好你好你好你好你好你好你好你好你好jdslajafsdkljfds你好你好你好你好你dsafasdfsfa好你好你好你好你好你好你好你好你好你好你好1')


if __name__ == '__main__':
    main()
