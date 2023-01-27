import sys
import os
from os import path
from pathlib import Path
import glob

sys.path.append(str(Path(path.abspath(__file__)).parent.parent.parent))
import model
import numpy as np
import cv2


class Typical_Pipeline:
    def __init__(self):
        self.OCR = model.Clova_OCR()
        self.re_OCR = model.Tesseract_OCR()
        self.MT = model.Papago_MT()
        self.Typical_Classification = model.FC("typical")

    def clova_ocr(self, image):
        encoded_img = np.fromstring(image, dtype=np.uint8)
        self.img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)

        merged_boxes = self.OCR.ocr(image)

        return merged_boxes

    def papago(self, text):
        _, en = self.MT.request(text)
        return en

    def typical_font_classification(self, merged_boxes):
        # tesseract + classification
        merged_boxes_with_crop = self.re_OCR.typical_ocr(merged_boxes, self.img)
        classified_font = self.Typical_Classification.classification(
            merged_boxes_with_crop
        )
        return classified_font



### example
# import pickle
# with open("/opt/Gobuk.pickle", 'rb') as f:
#     data = pickle.load(f)

# a = Typical_Pipeline()
# merged_boxes = a.clova_ocr(data)
# print("################")
# print(merged_boxes)
# print("################")

# en_list = []
# for i in merged_boxes:
#     en_list.append(a.papago(i[2]))

# print("################")
# print(en_list)
# print("################")

# classification_font = a.typical_font_classification(merged_boxes)

# print("################")
# print(classification_font)
# print("################")