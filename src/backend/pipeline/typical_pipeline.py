import sys
import os
from os import path
from typing import List
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

    def clova_ocr(self, bytes: bytes) -> List[List]:
        encoded_img = np.fromstring(bytes, dtype=np.uint8)
        self.img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)

        merged_boxes = self.OCR.ocr(bytes)

        return merged_boxes

    def papago(self, text: str) -> str:
        _, en = self.MT.request(text)
        return en

    def typical_font_classification(self, merged_boxes: List[List]) -> List[str]:
        """
        Args:
            merged_boxes: 아래와 같은 형태의 리스트
                ex)
                [
                    [[0, 0], [1, 1], "text"],
                    ...
                ]
        """
        # tesseract + classification
        merged_boxes_with_crop = self.re_OCR.n_divide(merged_boxes, self.img)
        classified_font = self.Typical_Classification.classification(
            merged_boxes_with_crop
        )
        return classified_font


### example
if __name__ == "__main__":
    import pickle

    with open("/opt/Gobuk.pickle", "rb") as f:
        data = pickle.load(f)

    a = Typical_Pipeline()
    merged_boxes = a.clova_ocr(data)
    print("######## merged_boxes ########")
    print(merged_boxes)
    print("##############################")

    en_list = []
    for i in merged_boxes:
        en_list.append(a.papago(i[2]))

    print("########## en_list ###########")
    print(en_list)
    print("##############################")

    classification_font = a.typical_font_classification(merged_boxes)

    print("#### classification_font #####")
    print(classification_font)
    print("##############################")
