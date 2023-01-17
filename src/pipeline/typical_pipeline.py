import sys
from os import path
sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))
import model
import numpy as np
import cv2

class Typical_Pipeline():
    
    def __init__(self):
        self.OCR = model.Clova_OCR()
        self.re_OCR = model.Tesseract_OCR()
        self.MT = model.Papago_MT()
        self.Classification = model.Typical_FC("typical_font")
        
    def clova_ocr(self, image):
        encoded_img = np.fromstring(image, dtype = np.uint8)
        self.img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
        
        merged_boxes = self.OCR.ocr(image)
        
        return merged_boxes
        
    def papago(self, text):
        ko, en = self.MT.request(text)
        return en
    
    def go(self, image):
        encoded_img = np.fromstring(image, dtype = np.uint8)
        self.img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
        
        merged_boxes = self.OCR.ocr(image)
        merged_boxes_with_crop = self.re_OCR.ocr(merged_boxes, self.img)
        classified_boxes = self.Classification.classification(merged_boxes_with_crop)
        result = self.MT.machine_translate(classified_boxes)
        
        # import pprint
        # pp = pprint.PrettyPrinter()
        # pp.pprint(result)
        return result
    