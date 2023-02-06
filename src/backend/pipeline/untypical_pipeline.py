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
        self.Font_Generator_mx_font = model.mx_eval
        self.Font_Generator_gas_font = model.gas_eval
        self.Font_Color = model.Font_Color()
        
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
        classified_font, classified_font_all = self.Typical_Classification.classification(
            merged_boxes_with_crop
        )
        font_color = self.Font_Color.find_color(merged_boxes_with_crop)
        
        return classified_font, classified_font_all, font_color

    def font_generate_mx_font(self, classified_font, en_list):
        self.Font_Generator_mx_font(classified_font, en_list)
        
    def font_generate_gasnext_font(self, classified_font, en_list):
        self.Font_Generator_gas_font(classified_font, en_list)
    def png2svg(self, generation_type):
        f = 100
        blur = 1
        t = 0.4

        base_str = ""
        for folder_path in glob.glob(os.path.join(os.getenv("HOME"), "tmp/*")):

            createDirectory(os.path.join(folder_path, f"generated_{generation_type}_svg"))
            for png_path in glob.glob(os.path.join(folder_path, f"generated_{generation_type}/*")):
                split_path, split_name = os.path.split(png_path)
                split_name = os.path.splitext(split_name)[0]
                base_str += f'convert {png_path} -flatten pgm:| mkbitmap -f {f} --blur {blur} -t {t} - -o -| \
                          potrace --svg -o {os.path.join(folder_path,f"generated_{generation_type}_svg", f"{split_name}.svg")}'
                base_str += " & "
        base_str += "wait"
        os.system(base_str)
 
 
    def svg2ttf(self,generation_type):
        ttf_list = []
        svgs2ttf_path = os.path.join(os.getenv("HOME"), "src/model/svg2ttf/svgs2ttf.py")
        example_json_path = os.path.join(
            os.getenv("HOME"), "src/model/svg2ttf/example.json"
        )
        base_str = ""
        for folder_path in glob.glob(os.path.join(os.getenv("HOME"), "tmp/*")):
            folder_name = os.path.basename(folder_path)
            with open(example_json_path, "r") as f:
                font_json = json.load(f)
            font_json["props"]["family"] = folder_name
            font_json["props"]["familyname"] = folder_name
            font_json["props"]["fontname"] = folder_name + "_Toon-ranslator"
            font_json["props"]["fullname"] = folder_name + "_Toon-ranslator_NTF"
            font_json["output"] = [os.path.join(folder_path, f"{folder_name}_{generation_type}.ttf")]
            ttf_list.append(font_json["output"])

            tmp = {}
            for svg_path in glob.glob(
                os.path.join(folder_path, f"generated_{generation_type}_svg/*")
            ):
                split_path, split_name = os.path.split(svg_path)
                split_name = os.path.splitext(split_name)[0]
                tmp[split_name] = {"src": svg_path, "width": 84}

            font_json["glyphs"] = tmp

            json_path = os.path.join(folder_path, f"{folder_name}.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(font_json, f, indent="\t")

            base_str += f"fontforge -lang=py -script {svgs2ttf_path} {json_path}"
            base_str += " & "
        base_str += "wait"
        os.system(base_str)

        return ttf_list