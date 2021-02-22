import cv2
import numpy as np
import json


def draw_field(image, field: dict):
    """Only using for visualising boxes"""
    shape = field["shape_attributes"]
    region = field["region_attributes"]

    color = (0, 255, 0) if "text" in region else (255, 0, 0)

    top_left = (shape["x"], shape["y"])
    bot_right = (shape["x"] + shape["width"], shape["y"] + shape["height"])

    cv2.rectangle(image, top_left, bot_right, color, thickness=3)


def display_label():
    front_template = cv2.imread("./template/front.png")

    with open("./template/front.json", "r", encoding="utf-8") as json_file:
        js = json.load(json_file)
        fields = js[list(js.keys())[0]]["regions"]

    for field in fields:
        # draw_field(front_template, field)
        shape = field["shape_attributes"]
        region = field["region_attributes"]

        color = (0, 255, 0) if "text" in region else (255, 0, 0)

        top_left = (shape["x"], shape["y"])
        bot_right = (shape["x"] + shape["width"], shape["y"] + shape["height"])
        if "text" not in region:
            cv2.rectangle(front_template, top_left, bot_right, color, thickness=3)

    cv2.imshow("Test", front_template)
    cv2.waitKey()


def main():
    display_label()


if __name__ == "__main__":
    main()
