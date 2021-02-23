from PIL import Image, ImageDraw, ImageFont
import numpy as np


class Converter:
    @staticmethod
    def pil2cv(image):
        return np.asarray(image)

    @staticmethod
    def cv2pil(image):
        # img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return Image.fromarray(img)


def put_text(
    image,
    text,
    shape: dict,
    font,
    text_size,
    text_color=(0, 0, 0),
    center_horizontal=False,
    center_vertical=False,
    x_offset=0,
    y_offset=0,
):
    draw = ImageDraw.Draw(image)
    fnt = ImageFont.truetype("./font_good_vie/{}.ttf".format(font), text_size)
    textsize = draw.textsize(text, fnt)

    # Get coords based on boundary
    textX = int(shape["x"] + (shape["width"] - textsize[0]) / 2) if center_horizontal else shape["x"]
    textY = (
        int(shape["y"] + (shape["height"] - textsize[1]) / 2)
        if center_vertical
        else int(shape["y"] + shape["height"] - textsize[1])
    )

    # Add text
    draw.text((textX + x_offset, textY + y_offset), text, font=fnt, fill=text_color)


def split_text(image, text, shape: dict, font, text_size):
    """Incase the text is too long, split it into 2 lines"""
    draw = ImageDraw.Draw(image)
    fnt = ImageFont.truetype("./font_good_vie/{}.ttf".format(font), text_size)

    shape_width = shape["width"]

    words = list(map(str.strip, text.split(" ")))

    for i in range(len(words)):
        textsize = draw.textsize(" ".join(words[:i]), fnt)
        if textsize[0] >= shape_width - 10:
            return (" ".join(words[: i - 1]), " ".join(words[i - 1 :]))

    return (text, "")


def get_concat_h_cut(im1, im2):
    dst = Image.new("RGB", (im1.width + im2.width, min(im1.height, im2.height)))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


def get_concat_v_cut(im1, im2):
    dst = Image.new("RGB", (min(im1.width, im2.width), im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


def get_concat_h_blank(im1, im2, color=(0, 0, 0)):
    dst = Image.new("RGB", (im1.width + im2.width, max(im1.height, im2.height)), color)
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


def get_concat_h_multi_blank(im_list):
    _im = im_list.pop(0)
    for im in im_list:
        _im = get_concat_h_blank(_im, im)
    return _im


def get_image_id_number(id_number):
    list_img_number = []
    numbers_path = "./so_cmnd/Bo_so_do_v1"
    for number in id_number:
        curr_image_path = "{}/{}.png".format(numbers_path, number)
        list_img_number.append(Image.open(curr_image_path))

    return get_concat_h_multi_blank(list_img_number)
