import cv2
import numpy as np
import json
import os
from tqdm import tqdm
import value_generator
from utils import Converter
from PIL import Image, ImageDraw, ImageFont
import utils
import constants


def visualise_template(template_name):
    # Load image and label path
    template_img_path = "./template/{}.png".format(template_name)
    template_label_path = "./template/{}.json".format(template_name)

    # Load the image
    template = cv2.imread(template_img_path)

    # Any color
    color = (0, 0, 255)

    with open(template_label_path, "r", encoding="utf-8") as json_file:
        js = json.load(json_file)
        fields = js[list(js.keys())[0]]["regions"]

        # Draw labels to images
        for field in fields:
            shape = field["shape_attributes"]
            region = field["region_attributes"]

            # Get bounding box positions
            top_left = (shape["x"], shape["y"])
            bot_left = (shape["x"], shape["y"] + shape["height"])
            bot_right = (shape["x"] + shape["width"], shape["y"] + shape["height"])

            # Draw the label
            if "text" not in region:
                cv2.rectangle(template, top_left, bot_right, color, thickness=3)
                cv2.putText(template, region["key_type"], bot_left, cv2.FONT_HERSHEY_COMPLEX, 1.1, (0, 0, 0))

    # Save the visualise
    cv2.imwrite("./visualise_labels/{}_labels.jpg".format(template_name), template)


def gen_front_cmt():
    template_name = "front"

    # Load image and label path
    template_img_path = "./template/{}.png".format(template_name)
    template_label_path = "./template/{}.json".format(template_name)

    template = Image.open(template_img_path)

    # Random data
    id_number = value_generator.gen_idnumber()
    ho_ten = value_generator.gen_fullname()
    ngay_sinh = value_generator.gen_birthday()
    nguyen_quan = value_generator.gen_hometown()
    hktt = value_generator.gen_current_place()

    # Put data to each box
    with open(template_label_path, "r", encoding="utf-8") as json_file:
        js = json.load(json_file)
        fields = js[list(js.keys())[0]]["regions"]

        # Draw labels to images
        for field in fields:
            shape = field["shape_attributes"]
            region = field["region_attributes"]

            # Get bounding box positions
            top_left = (shape["x"], shape["y"])
            bot_left = (shape["x"], shape["y"] + shape["height"])
            top_right = (shape["x"] + shape["width"], shape["y"])
            bot_right = (shape["x"] + shape["width"], shape["y"] + shape["height"])

            # Get key type of the field
            key_type = region["key_type"]

            # ID Number
            if key_type == "id":
                utils.put_text(
                    template,
                    id_number,
                    shape,
                    "arial",
                    32,
                    text_color=constants.ID_NUMBER[-1],
                    center_horizontal=True,
                    center_vertical=True,
                    y_offset=-4,
                )
            # Fullname
            elif key_type in ["ho_ten_1", "ho_ten_2"]:
                is_first_line = key_type == "ho_ten_1"
                if is_first_line:
                    ho_ten_1, ho_ten_2 = utils.split_text(template, ho_ten, shape, "Times New Roman", 28)
                utils.put_text(
                    template,
                    ho_ten_1 if key_type == "ho_ten_1" else ho_ten_2,
                    shape,
                    "Times New Roman",
                    28,
                    center_horizontal=is_first_line,
                )
            # Birthday
            elif key_type == "ngay_sinh":
                utils.put_text(template, ngay_sinh, shape, "Times New Roman", 28, center_horizontal=True)
            # Hometown
            elif key_type in ["nguyen_quan_1", "nguyen_quan_2"]:
                is_first_line = key_type == "nguyen_quan_1"
                if is_first_line:
                    nguyen_quan_1, nguyen_quan_2 = utils.split_text(template, nguyen_quan, shape, "Times New Roman", 28)
                utils.put_text(
                    template,
                    nguyen_quan_1 if key_type == "nguyen_quan_1" else nguyen_quan_2,
                    shape,
                    "Times New Roman",
                    28,
                    center_horizontal=is_first_line,
                )
            # Place to live
            elif key_type in ["ho_khau_thuong_tru_1", "ho_khau_thuong_tru_2"]:
                is_first_line = key_type == "ho_khau_thuong_tru_1"
                if is_first_line:
                    hktt_1, hktt_2 = utils.split_text(template, hktt, shape, "Times New Roman", 28)
                utils.put_text(
                    template,
                    hktt_1 if key_type == "ho_khau_thuong_tru_1" else hktt_2,
                    shape,
                    "Times New Roman",
                    28,
                    center_horizontal=is_first_line,
                )

        template.show()


def save_all_visualise_label():
    for template in tqdm(os.listdir("./template")):
        template_name = template.split(".")[0]
        template_img = "{}.png".format(template_name)
        template_label = "{}.json".format(template_name)
        if template_img not in os.listdir("./template") or template_label not in os.listdir("./template"):
            continue

        ext = template.split(".")[-1]
        if ext != "png":
            continue

        print(template_name)
        visualise_template(template_name)


def main():
    gen_front_cmt()


if __name__ == "__main__":
    main()
