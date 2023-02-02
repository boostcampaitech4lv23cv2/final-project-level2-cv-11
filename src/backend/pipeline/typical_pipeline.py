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
        self.re_OCR = model.Tesseract_OCR("typical")
        self.MT = model.Papago_MT()
        self.Typical_Classification = model.FC("typical")
        self.Font_Color = model.Font_Color()

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
        font_color = self.Font_Color.find_color(merged_boxes_with_crop)
        return classified_font, font_color