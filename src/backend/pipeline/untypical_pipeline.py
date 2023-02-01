import sys
import os
from os import path
from pathlib import Path
import glob
import json

sys.path.append(str(Path(path.abspath(__file__)).parent.parent.parent))
import model
import numpy as np
import cv2


def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")


class Untypical_Pipeline:
    def __init__(self, git_path):
        os.environ["HOME"] = git_path
        self.OCR = model.Clova_OCR()
        self.re_OCR = model.Tesseract_OCR("untypical")
        self.MT = model.Papago_MT()
        self.Typical_Classification = model.FC("untypical")
        self.Font_Generator_mx_font = model.eval

    def clova_ocr(self, image):
        encoded_img = np.fromstring(image, dtype=np.uint8)
        self.img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)

        merged_boxes = self.OCR.ocr(image)

        return merged_boxes

    def papago(self, text):
        _, en = self.MT.request(text)
        return en

    def untypical_font_classification(self, merged_boxes):
        # tesseract + classification
        merged_boxes_with_crop = self.re_OCR.n_divide(merged_boxes, self.img)
        classified_font = self.Typical_Classification.classification(
            merged_boxes_with_crop
        )
        return classified_font

    def font_generate_mx_font(self, classified_font, en_list):
        self.Font_Generator_mx_font(classified_font, en_list)

    def png2svg(self):
        for folder_path in glob.glob(os.path.join(os.getenv("HOME"), "tmp/*")):
            for png_path in glob.glob(os.path.join(folder_path, "generated_mxfont/*")):
                split_path, split_name = os.path.split(png_path)
                split_name = os.path.splitext(split_name)[0]
                createDirectory(os.path.join(folder_path, "generated_mxfont_svg"))
                os.system(
                    f'convert {png_path} -flatten pgm:| mkbitmap -f 64 -t 0.4 - -o -| \
                          potrace --svg -o {os.path.join(folder_path,"generated_mxfont_svg", f"{split_name}.svg")}'
                )

    def svg2ttf(self):
        ttf_list = []
        svgs2ttf_path = os.path.join(os.getenv("HOME"), "src/model/svg2ttf/svgs2ttf.py")
        example_json_path = os.path.join(
            os.getenv("HOME"), "src/model/svg2ttf/example.json"
        )

        for folder_path in glob.glob(os.path.join(os.getenv("HOME"), "tmp/*")):
            folder_name = os.path.basename(folder_path)
            with open(example_json_path, "r") as f:
                font_json = json.load(f)
            font_json["props"]["family"] = folder_name
            font_json["props"]["familyname"] = folder_name
            font_json["props"]["fontname"] = folder_name + "_Toon-ranslator"
            font_json["props"]["fullname"] = folder_name + "_Toon-ranslator_NTF"
            font_json["output"] = [os.path.join(folder_path, f"{folder_name}.ttf")]
            ttf_list.append(font_json["output"])

            tmp = {}
            for svg_path in glob.glob(
                os.path.join(folder_path, "generated_mxfont_svg/*")
            ):
                split_path, split_name = os.path.split(svg_path)
                split_name = os.path.splitext(split_name)[0]
                tmp[split_name] = {"src": svg_path, "width": 128}

            font_json["glyphs"] = tmp

            json_path = os.path.join(folder_path, f"{folder_name}.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(font_json, f, indent="\t")

            os.system(f"fontforge -lang=py -script {svgs2ttf_path} {json_path}")

        return ttf_list


## example
if __name__ == "__main__":
    import pickle

    with open("/opt/final-project-level2-cv-11/대학원탈출_전형_v2.png", "rb") as f:
        data = f.read()
    a = Untypical_Pipeline("/opt/final-project-level2-cv-11")
    merged_boxes = a.clova_ocr(data)
    print("################")
    print(merged_boxes)
    print("################")

    en_list = []
    for i in merged_boxes:
        en_list.append(a.papago(i[2]))

    print("################")
    print(en_list)
    print("################")

    classification_font = a.untypical_font_classification(merged_boxes)

    print("################")
    print(classification_font)
    print("################")

    a.font_generate_mx_font(classification_font, en_list)
    a.png2svg()
    print(a.svg2ttf())
